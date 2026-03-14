import { tool } from "@opencode-ai/plugin";
import TurndownService from "turndown";
import path from "path";
import fs from "fs";
const LOG_FILE = "/tmp/google-ai-search.log";
function log(msg) {
    const line = `[${new Date().toISOString()}] ${msg}\n`;
    fs.appendFileSync(LOG_FILE, line);
}
function expandHomeDir(dir) {
    if (dir.startsWith("~/")) {
        return path.join(process.env.HOME || "", dir.slice(2));
    }
    return dir;
}
async function findLatestProfile(chromePath) {
    try {
        if (!fs.existsSync(chromePath))
            return null;
        const entries = fs.readdirSync(chromePath, { withFileTypes: true });
        const profiles = entries
            .filter(e => e.isDirectory() && (e.name === "Default" || e.name.startsWith("Profile")))
            .map(e => ({
            name: e.name,
            path: path.join(chromePath, e.name),
            mtime: fs.statSync(path.join(chromePath, e.name)).mtime.getTime()
        }))
            .sort((a, b) => b.mtime - a.mtime);
        return profiles[0]?.path ?? null;
    }
    catch {
        return null;
    }
}
const DEFAULT_TIMEOUT = 30_000;
const MAX_TIMEOUT = 120_000;
export const GoogleAISearchPlugin = async () => {
    const GoogleAITool = tool({
        description: "Search the web using Google's AI-powered search mode. This tool provides comprehensive, AI-enhanced search results with contextual information, summaries, and source references. Use this for any web searches, current events, factual lookups, research questions, or when you need up-to-date information beyond your knowledge cutoff. Returns structured markdown responses with sources.",
        args: {
            query: tool.schema.string().describe("Question or topic to submit to Google AI Mode"),
            timeout: tool.schema
                .number()
                .min(5)
                .max(120)
                .optional()
                .describe("Timeout in seconds (default: 30, max: 120)"),
            followUp: tool.schema
                .boolean()
                .optional()
                .describe("Treat the query as a follow-up in the same session"),
        },
        async execute(params, ctx) {
            const playwright = await loadPlaywright();
            const manager = new GoogleAIModeManager(playwright);
            const timeoutMs = Math.min((params.timeout ?? DEFAULT_TIMEOUT / 1000) * 1000, MAX_TIMEOUT);
            const abortHandler = () => {
                manager.dispose().catch(() => undefined);
            };
            ctx.abort.addEventListener("abort", abortHandler, { once: true });
            try {
                const result = await manager.query(params.query, params.followUp ?? false, timeoutMs, ctx.abort);
                ctx.metadata({
                    title: `Google AI: ${params.query}`,
                    metadata: {
                        query: params.query,
                        sourceCount: result.sources.count,
                        responseTime: result.metadata.responseTime,
                        hasTable: result.tableData.length > 0,
                    },
                });
                return formatAIResponse(result);
            }
            catch (error) {
                const message = error.message;
                if (message.includes("Timeout") || message.includes("forSelector")) {
                    throw new Error("Google AI Mode unavailable: automated access is currently blocked. This is expected behaviour.");
                }
                throw error;
            }
            finally {
                ctx.abort.removeEventListener("abort", abortHandler);
                await manager.dispose();
            }
        },
    });
    return {
        tool: {
            google_ai_search_plus: GoogleAITool,
        },
    };
};
async function loadPlaywright() {
    log("Loading playwright...");
    try {
        const pw = await import("playwright");
        log("Playwright loaded from default");
        return pw;
    }
    catch (error) {
        const err = error;
        const paths = [
            "/Users/francisco/.config/opencode/node_modules/playwright",
            "/Users/francisco/.config/Opencode-Google-AI-Search-Plugin/node_modules/playwright",
            "./node_modules/playwright",
        ];
        for (const p of paths) {
            try {
                log(`Trying to load playwright from: ${p}`);
                const pw = await import(p);
                log(`Playwright loaded from: ${p}`);
                return pw;
            }
            catch { }
        }
        throw new Error(`google_ai_search_plus requires Playwright. Install it with: bun install playwright && bunx playwright install chromium. Error: ${err.message}`);
    }
}
class GoogleAIModeManager {
    playwright;
    browser = null;
    page = null;
    conversationActive = false;
    sessionStartTime = Date.now();
    SESSION_TIMEOUT = 5 * 60 * 1000;
    constructor(playwright) {
        this.playwright = playwright;
    }
    async query(query, followUp, timeout, abortSignal) {
        log(`Starting query: ${query}`);
        if (Date.now() - this.sessionStartTime > this.SESSION_TIMEOUT) {
            await this.reset();
        }
        await this.ensureBrowserSession();
        if (!followUp || !this.conversationActive) {
            await this.navigateToAIMode();
            this.conversationActive = true;
        }
        return await this.submitQuery(query, timeout, abortSignal);
    }
    async ensureBrowserSession() {
        log("=== Starting browser session ===");
        if (!this.browser) {
            try {
                log("Attempting to connect to existing Chrome via CDP...");
                this.browser = await this.playwright.chromium.connectOverCDP("http://127.0.0.1:9222");
                log("Connected to existing Chrome via CDP!");
            }
            catch (e) {
                log(`Could not connect to Chrome via CDP (${e}), trying profile...`);
                const chromeProfilePath = expandHomeDir("~/Library/Application Support/Google/Chrome");
                log(`Looking for Chrome profile in: ${chromeProfilePath}`);
                try {
                    const userDataDir = await findLatestProfile(chromeProfilePath);
                    log(`Found profile: ${userDataDir}`);
                    if (userDataDir) {
                        log(`Using Chrome profile with launchPersistentContext: ${userDataDir}`);
                        try {
                            const context = await this.playwright.chromium.launchPersistentContext(userDataDir, {
                                headless: true,
                                args: [
                                    "--no-sandbox",
                                    "--disable-dev-shm-usage",
                                    "--disable-blink-features=AutomationControlled",
                                    "--disable-features=VizDisplayCompositor",
                                ],
                            });
                            this.browser = context.browser();
                            log("Browser launched with profile - SUCCESS");
                        }
                        catch (e3) {
                            log(`launchPersistentContext failed: ${e3}`);
                            throw e3;
                        }
                    }
                }
                catch (e2) {
                    log(`Could not use Chrome profile, launching new browser: ${e2}`);
                    this.browser = await this.playwright.chromium.launch({
                        headless: true,
                        args: [
                            "--no-sandbox",
                            "--disable-dev-shm-usage",
                            "--disable-blink-features=AutomationControlled",
                            "--disable-features=VizDisplayCompositor",
                        ],
                    });
                }
            }
        }
        if (!this.page) {
            const contexts = this.browser.contexts();
            if (contexts.length > 0) {
                this.page = await contexts[0].newPage();
            }
            else {
                this.page = await this.browser.newPage();
            }
            this.page.on("console", msg => log("Browser console: " + msg.type() + " " + msg.text()));
            this.page.on("pageerror", err => log("Browser error: " + err.message));
            await this.page.addInitScript(() => {
                Object.defineProperty(navigator, "webdriver", {
                    get: () => false,
                });
                const chrome = window.chrome;
                if (chrome?.runtime?.onConnect) {
                    delete chrome.runtime.onConnect;
                }
                Object.defineProperty(navigator, "languages", {
                    get: () => ["en-GB", "en-US", "en"],
                });
            });
        }
        log("=== Browser session ready ===");
    }
    async navigateToAIMode() {
        if (!this.page)
            throw new Error("Page not initialized");
        await this.page.goto("https://www.google.com");
        await this.page.waitForTimeout(2000);
    }
    buildAIModeURL(query) {
        const baseURL = "https://www.google.com/search";
        const params = new URLSearchParams({
            udm: "50",
            aep: "22",
            q: query ?? "",
            hl: "en",
        });
        return `${baseURL}?${params.toString()}`;
    }
    async submitQuery(query, timeout, abortSignal) {
        if (!this.page)
            throw new Error("Page not initialized");
        const startTime = Date.now();
        const aiModeUrl = this.buildAIModeURL(query);
        await this.page.goto(aiModeUrl, { waitUntil: "networkidle", timeout });
        if (this.page.url().includes("/sorry/")) {
            throw new Error("Google is blocking automated access.");
        }
        await this.page.waitForTimeout(3000);
        let previousLength = 0;
        let stableCount = 0;
        const waitStartTime = Date.now();
        const maxWaitTime = timeout;
        while (Date.now() - waitStartTime < maxWaitTime) {
            await this.page.waitForTimeout(2000);
            const currentLength = await this.page.evaluate(() => document.body.textContent?.length ?? 0);
            if (currentLength === previousLength) {
                stableCount += 1;
                if (stableCount >= 3) {
                    break;
                }
            }
            else {
                stableCount = 0;
            }
            previousLength = currentLength;
        }
        const hasContent = await this.page.evaluate(() => {
            const body = document.body.textContent ?? "";
            return (body.includes("AI responses may include mistakes") ||
                !!document.querySelector("table") ||
                body.length > 10_000);
        });
        if (!hasContent) {
            throw new Error("AI content did not load");
        }
        const response = await this.parseResponse(query, Date.now() - startTime);
        if (abortSignal.aborted) {
            throw new Error("Operation aborted");
        }
        return response;
    }
    async parseResponse(query, responseTime) {
        if (!this.page)
            throw new Error("Page not initialized");
        const extraction = await this.page.evaluate(() => {
            const clean = (text) => {
                if (!text)
                    return "";
                return text
                    .replace(/\u00a0/g, " ")
                    .replace(/\r\n?/g, "\n")
                    .replace(/[\t ]+\n/g, "\n")
                    .replace(/\n[\t ]+/g, "\n")
                    .replace(/[ \t]{2,}/g, " ")
                    .replace(/\n{3,}/g, "\n\n")
                    .replace(/\s([,:;.!?])/g, "$1")
                    .trim();
            };
            const root = document.querySelector('[data-aimmrs="true"]') ||
                document.querySelector("#aim-chrome-initial-inline-async-container") ||
                document.querySelector('[data-aim-chrome-rendered="true"]') ||
                document.body;
            const main = root.querySelector(".mZJni.Dn7Fzd") || root;
            const contentContainer = main.querySelector(".Zkbeff") || main;
            const blockSelectors = "[role=\"heading\"], h1, h2, h3, h4, h5, h6, .Y3BBE, .Fv6NCb, table, ul, ol, p";
            const orderedNodes = Array.from(contentContainer.querySelectorAll(blockSelectors));
            const blocks = [];
            const listHeadingMarkers = new Set();
            const paragraphTexts = new Set();
            let summary = "";
            let tableBlock = null;
            const shouldSkipText = (text) => {
                if (!text)
                    return true;
                if (/AI responses may include mistakes/i.test(text))
                    return true;
                if (/learn more$/i.test(text))
                    return true;
                return false;
            };
            orderedNodes.forEach((node) => {
                const text = clean(node.innerText);
                if (shouldSkipText(text)) {
                    return;
                }
                if (node.classList.contains("otQkpb") || node.matches("[role=\"heading\"], h1, h2, h3, h4, h5, h6")) {
                    const level = parseInt(node.getAttribute("aria-level") || "3", 10);
                    blocks.push({ type: "heading", text, level });
                    return;
                }
                if (node.classList.contains("Fv6NCb")) {
                    const table = node.querySelector("table");
                    if (table) {
                        const rows = Array.from(table.querySelectorAll("tr")).map((row) => Array.from(row.querySelectorAll("th,td")).map((cell) => clean(cell.innerText))).filter((row) => row.some((cell) => cell));
                        if (rows.length > 1) {
                            tableBlock = {
                                header: rows[0],
                                rows: rows.slice(1),
                            };
                            blocks.push({ type: "table" });
                        }
                    }
                    return;
                }
                if (node.tagName === "UL" || node.tagName === "OL") {
                    const items = Array.from(node.querySelectorAll(":scope > li"))
                        .map((li) => clean(li.innerText))
                        .filter(Boolean);
                    if (items.length === 0)
                        return;
                    let heading;
                    const prev = node.previousElementSibling;
                    if (prev && listHeadingMarkers.has(prev)) {
                        heading = clean(prev.innerText).replace(/:\s*$/, "");
                    }
                    blocks.push({
                        type: "list",
                        ordered: node.tagName === "OL",
                        heading,
                        items,
                    });
                    return;
                }
                if (node.classList.contains("Y3BBE") || node.tagName === "P") {
                    if (node.tagName === "P" && node.closest("li")) {
                        return;
                    }
                    if (!summary) {
                        summary = text;
                    }
                    const next = node.nextElementSibling;
                    if (next && (next.tagName === "UL" || next.tagName === "OL")) {
                        listHeadingMarkers.add(node);
                        return;
                    }
                    if (!paragraphTexts.has(text)) {
                        paragraphTexts.add(text);
                        blocks.push({ type: "paragraph", text });
                    }
                }
            });
            if (!summary) {
                summary = clean(contentContainer.innerText.split("\n").find(Boolean) || "");
            }
            const rawHtml = contentContainer.innerHTML;
            const rawText = clean(contentContainer.innerText);
            const fallbackParagraphs = rawText
                .split(/\n{2,}/)
                .map((part) => clean(part))
                .filter((value) => value.length > 0);
            const consentIndicators = [
                "Before you continue to Google Search",
                "We use cookies",
                "By using our services, you agree",
                "We value your privacy",
            ];
            const isConsent = consentIndicators.some((phrase) => root.innerText.includes(phrase));
            const sourceContainer = root.querySelector(".ofHStc");
            let sourceCount = 0;
            const sources = [];
            let hasVideo = false;
            if (sourceContainer) {
                const countMatch = sourceContainer.innerText.match(/(\d+)\s+sites?/i);
                if (countMatch) {
                    sourceCount = parseInt(countMatch[1], 10);
                }
                const list = sourceContainer.querySelector("ul");
                if (list) {
                    const seenLinks = new Set();
                    Array.from(list.querySelectorAll(":scope > li")).forEach((li) => {
                        const itemText = clean(li.innerText);
                        const link = li.querySelector("a")?.href || undefined;
                        if (/sites?$/i.test(itemText)) {
                            return;
                        }
                        if (link) {
                            if (seenLinks.has(link))
                                return;
                            seenLinks.add(link);
                        }
                        const lines = itemText.split("\n").map((part) => part.trim()).filter(Boolean);
                        const titleLine = lines[0] || itemText;
                        if (/YouTube/i.test(itemText)) {
                            hasVideo = true;
                        }
                        const publisherMatch = lines.length > 1 ? lines[lines.length - 1] : undefined;
                        sources.push({
                            title: titleLine,
                            url: link,
                            publisher: publisherMatch && publisherMatch !== titleLine ? publisherMatch : undefined,
                        });
                    });
                }
            }
            if (!sourceCount && sources.length > 0) {
                sourceCount = sources.length;
            }
            return {
                summary,
                blocks,
                table: tableBlock,
                rawHtml,
                rawText,
                fallbackParagraphs,
                isConsent,
                sources: {
                    count: sourceCount,
                    entries: sources,
                    hasVideo,
                },
            };
        });
        const answerSections = [];
        const tableRows = [];
        const tableHeaders = (extraction.table?.header ?? []).slice(0, 3);
        extraction.blocks?.forEach((block) => {
            if (!block || !block.type)
                return;
            if (block.type === "heading" && block.text) {
                const level = Math.min(6, Math.max(3, block.level || 3));
                const prefix = "#".repeat(level);
                answerSections.push(`${prefix} ${block.text}`);
                return;
            }
            if (block.type === "paragraph" && block.text) {
                answerSections.push(block.text);
                return;
            }
            if (block.type === "list" && Array.isArray(block.items)) {
                if (block.heading) {
                    answerSections.push(`**${block.heading}:**`);
                }
                block.items.forEach((item) => {
                    answerSections.push(`- ${item}`);
                });
                return;
            }
            if (block.type === "table" && extraction.table) {
                const headers = (extraction.table.header || []).slice(0, 3);
                const rows = (extraction.table.rows || []);
                if (headers.length >= 2 && rows.length > 0) {
                    const headerLine = `| ${headers.join(" | ")} |`;
                    const separator = `|${headers.map(() => "---").join("|")}|`;
                    const body = rows.map((row) => `| ${headers.map((_, idx) => row[idx] || "").join(" | ")} |`);
                    answerSections.push(headerLine);
                    answerSections.push(separator);
                    answerSections.push(...body);
                    rows.forEach((row) => {
                        tableRows.push({
                            feature: row[0] || "",
                            column1: row[1] || "",
                            column2: row[2] || "",
                        });
                    });
                }
            }
        });
        const summary = extraction.summary || "";
        if (summary && !answerSections.find((section) => section.includes(summary))) {
            answerSections.unshift(summary);
        }
        const formattedAnswer = answerSections
            .filter((section) => section && section.trim())
            .join("\n\n");
        const sourceEntries = (extraction.sources?.entries ?? []);
        const sourceNames = sourceEntries
            .map((entry) => entry.publisher)
            .filter((name) => Boolean(name));
        const uniqueSites = Array.from(new Set(sourceNames));
        let finalAnswer = formattedAnswer;
        const fallbackContent = (extraction.fallbackParagraphs ?? [])
            .filter((paragraph) => paragraph.length > 40)
            .filter((paragraph) => !finalAnswer.includes(paragraph.slice(0, Math.min(60, paragraph.length))));
        if ((!finalAnswer || finalAnswer.length < 500) && fallbackContent.length > 0) {
            const fallbackBlock = fallbackContent.join("\n\n");
            finalAnswer = finalAnswer ? `${finalAnswer}\n\n---\n${fallbackBlock}` : fallbackBlock;
        }
        if (extraction.isConsent) {
            finalAnswer = formattedAnswer || extraction.rawText || finalAnswer;
        }
        let markdownAnswer = "";
        const turndownService = new TurndownService({
            headingStyle: "atx",
            hr: "---",
            bulletListMarker: "-",
            codeBlockStyle: "fenced",
            emDelimiter: "*",
        });
        turndownService.remove(["script", "style", "meta", "link"]);
        if (extraction.rawHtml) {
            try {
                markdownAnswer = turndownService.turndown(extraction.rawHtml);
            }
            catch {
                markdownAnswer = "";
            }
        }
        if (markdownAnswer && fallbackContent.length > 0) {
            const fallbackBlock = fallbackContent.join("\n\n");
            if (fallbackBlock && !markdownAnswer.includes(fallbackBlock.slice(0, Math.min(80, fallbackBlock.length)))) {
                markdownAnswer = `${markdownAnswer}\n\n---\n${fallbackBlock}`;
            }
        }
        if (!markdownAnswer || markdownAnswer.trim().length < 200) {
            markdownAnswer = finalAnswer;
        }
        if (!markdownAnswer && extraction.rawText) {
            markdownAnswer = extraction.rawText;
        }
        return {
            query,
            answer: markdownAnswer || summary || `Google AI response for: ${query}`,
            summary,
            tableData: tableRows,
            tableHeaders,
            sources: {
                count: extraction.sources?.count ?? sourceEntries.length,
                hasVideo: Boolean(extraction.sources?.hasVideo),
                sites: uniqueSites,
                references: sourceEntries,
            },
            metadata: {
                responseTime,
                conversationIndex: this.conversationActive ? 2 : 1,
                sessionId: `session_${this.sessionStartTime}`,
                timestamp: new Date(),
            },
        };
    }
    async reset() {
        this.conversationActive = false;
        this.sessionStartTime = Date.now();
        try {
            if (this.page) {
                await this.page.getByRole("button", { name: "Start new search" }).click({ timeout: 2000 });
            }
        }
        catch {
            if (this.page) {
                await this.page.goto("https://www.google.com", { waitUntil: "load" });
            }
        }
    }
    async dispose() {
        if (this.page) {
            await this.page.close().catch(() => undefined);
            this.page = null;
        }
        if (this.browser) {
            await this.browser.close().catch(() => undefined);
            this.browser = null;
        }
        this.conversationActive = false;
    }
}
function formatAIResponse(response) {
    let output = `# ${response.query}\n\n`;
    if (response.summary && response.summary !== response.answer) {
        output += `**Summary**: ${response.summary}\n\n`;
    }
    output += `## Answer\n\n${response.answer}\n\n`;
    if (response.tableData && response.tableData.length > 0) {
        const headers = response.tableHeaders && response.tableHeaders.length >= 3
            ? response.tableHeaders.slice(0, 3)
            : ["Feature", "Option 1", "Option 2"];
        const signature = `| ${headers[0]} | ${headers[1]} |`;
        const alreadyPresent = response.answer.includes(signature);
        if (!alreadyPresent) {
            output += `## Comparison Table\n\n`;
            output += `| ${headers.join(" | ")} |\n`;
            output += `|${headers.map(() => "---").join("|")}|\n`;
            response.tableData.forEach((row) => {
                const values = [row.feature, row.column1, row.column2];
                output += `| ${headers.map((_, idx) => values[idx] || "").join(" | ")} |\n`;
            });
            output += "\n";
        }
    }
    output += "## Sources\n\n";
    output += `- **Sources Referenced**: ${response.sources.count} sites\n`;
    if (response.sources.hasVideo) {
        output += "- **Includes Video Sources**: Yes\n";
    }
    output += `- **Response Time**: ${response.metadata.responseTime}ms\n`;
    output += `- **Session**: ${response.metadata.sessionId}\n`;
    if (response.sources.references && response.sources.references.length > 0) {
        output += "- **Source Links:**\n";
        response.sources.references.forEach((ref) => {
            if (!ref?.title)
                return;
            const label = ref.url ? `[${ref.title}](${ref.url})` : ref.title;
            output += `  - ${label}\n`;
        });
    }
    return output;
}
export default GoogleAISearchPlugin;
//# sourceMappingURL=index.js.map
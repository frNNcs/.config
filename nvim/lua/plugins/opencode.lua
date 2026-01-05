return {
    "NickvanDyke/opencode.nvim",
    dependencies = {
        -- Recommended for input/picker support and required for the `snacks` provider
        { "folke/snacks.nvim", opts = { input = {}, picker = {}, terminal = {} } },
    },
    config = function()
        -- Use defaults (see `:help opencode` or lua/opencode/config.lua for options)
        vim.g.opencode_opts = {}

        -- Required for `opts.events.reload` so buffers are reloaded when opencode edits files
        vim.o.autoread = true

        -- Example keymaps (opt-in, choose what you like)
        vim.keymap.set({ "n", "x" }, "<leader>oa", function()
            require("opencode").ask("@this: ", { submit = true })
        end, { desc = "Ask opencode" })

        vim.keymap.set({ "n", "x" }, "<leader>ox", function()
            require("opencode").select()
        end, { desc = "Execute opencode action…" })

        vim.keymap.set({ "n", "t" }, "<leader>ot", function()
            require("opencode").toggle()
        end, { desc = "Toggle opencode" })

        -- Operator mappings (supports ranges and dot-repeat)
        vim.keymap.set({ "n", "x" }, "go", function()
            return require("opencode").operator("@this ")
        end, { expr = true, desc = "Add range to opencode" })

        vim.keymap.set("n", "goo", function()
            return require("opencode").operator("@this ") .. "_"
        end, { expr = true, desc = "Add line to opencode" })

        -- handy scrolling commands for opencode sessions
        vim.keymap.set("n", "<S-C-u>", function()
            require("opencode").command("session.half.page.up")
        end, { desc = "opencode half page up" })

        vim.keymap.set("n", "<S-C-d>", function()
            require("opencode").command("session.half.page.down")
        end, { desc = "opencode half page down" })
    end,
}

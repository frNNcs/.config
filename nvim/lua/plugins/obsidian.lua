return {
  {
    "epwalsh/obsidian.nvim",
    dependencies = { "nvim-lua/plenary.nvim", "nvim-telescope/telescope.nvim", "nvim-tree/nvim-web-devicons" },
    ft = { "markdown" },
    config = function()
      local home = os.getenv("HOME") or vim.fn.expand("~")
      local env_vault = vim.fn.getenv("OBSIDIAN_VAULT")

      local vaults = {
        vim.fn.expand("~/projects/homelab/DATA/syncthing/obsidian/002 Areas/work/Banco Ciudad"),
        vim.fn.expand("~/projects/homelab/DATA/syncthing/obsidian"),
      }

      if env_vault and env_vault ~= "" then
        table.insert(vaults, 1, env_vault)
      end

      local current_vault = vaults[1]

      local function setup_obsidian(dir)
        -- prefer already-loaded module
        local ok, obs = pcall(require, "obsidian")
        if not ok or not obs then
          -- try to load plugin dynamically via lazy.nvim if available
          if pcall(require, "lazy") and require("lazy").load then
            pcall(function()
              require("lazy").load({ plugins = { "epwalsh/obsidian.nvim" } })
            end)
            ok, obs = pcall(require, "obsidian")
          end
        end
        if not ok or not obs then
          vim.notify("obsidian.nvim not available yet; run :Lazy sync or open a markdown file to load it", vim.log.levels.WARN)
          return false
        end

        obs.setup({
          dir = vim.fn.expand(dir),
          completion = { nvim_cmp = true, enabled = true },
          note_frontmatter_func = nil,
          daily_notes = { folder = "daily" },
          follow_url = true,
        })
        current_vault = dir
        vim.notify("Obsidian vault set to: " .. dir, vim.log.levels.INFO)
        return true
      end

      -- Try initial setup but don't error if plugin not installed yet
      pcall(setup_obsidian, current_vault)

      -- User commands to list and switch vaults
      vim.api.nvim_create_user_command("ObsidianListVaults", function()
        print("Available Obsidian vaults:")
        for i, v in ipairs(vaults) do
          print(i .. ": " .. v)
        end
      end, {})

      vim.api.nvim_create_user_command("ObsidianSwitchVault", function(opts)
        local arg = opts.args
        if arg == nil or arg == "" then
          print("Usage: :ObsidianSwitchVault <path|index>")
          return
        end
        local target = nil
        local idx = tonumber(arg)
        if idx then
          target = vaults[idx]
        else
          for _, v in ipairs(vaults) do
            if v == arg then
              target = v
              break
            end
          end
        end
        if not target then
          print("Vault not found: " .. arg)
          return
        end
        setup_obsidian(target)
      end, { nargs = 1, complete = function(ArgLead)
        local res = {}
        for _, v in ipairs(vaults) do
          if v:sub(1, #ArgLead) == ArgLead then
            table.insert(res, v)
          end
        end
        return res
      end })

      -- Keymaps (lazy-load plugin if needed)
      vim.keymap.set("n", "<leader>on", function()
        if not pcall(function() return require("obsidian") end) then
          if pcall(require, "lazy") then
            require("lazy").load({ plugins = { "epwalsh/obsidian.nvim" } })
          end
        end
        local ok, obs = pcall(require, "obsidian")
        if ok and obs then
          obs.new({ title = "" })
        else
          print("obsidian.nvim not available; run :Lazy sync to install it")
        end
      end, { desc = "Obsidian: new note" })

      vim.keymap.set("n", "<leader>od", function()
        if not pcall(function() return require("obsidian") end) then
          if pcall(require, "lazy") then
            require("lazy").load({ plugins = { "epwalsh/obsidian.nvim" } })
          end
        end
        local ok, dailies = pcall(require, "obsidian.dailies")
        if ok and dailies then
          dailies.new()
        else
          print("obsidian.dailies not available; run :Lazy sync to install obsidian.nvim")
        end
      end, { desc = "Obsidian: new daily note" })

      -- Telescope integration (if available)
      if pcall(require, "telescope") then
        local has_obs_tel = pcall(function()
          return require("telescope._extensions.obsidian")
        end)
        vim.keymap.set("n", "<leader>os", function()
          if has_obs_tel then
            require("telescope").extensions.obsidian.obsidian({})
          else
            local opts = { "Choose a vault:" }
            for i, v in ipairs(vaults) do
              table.insert(opts, i .. ": " .. v)
            end
            local choice = vim.fn.inputlist(opts)
            if choice and choice >= 1 and choice <= #vaults then
              setup_obsidian(vaults[choice])
            end
          end
        end, { desc = "Obsidian: search (telescope) or switch vault" })
      else
        vim.keymap.set("n", "<leader>os", function()
          print("Telescope not available: install nvim-telescope/telescope.nvim for search")
        end, { desc = "Obsidian: search (telescope)" })
      end

      -- If obsidian isn't installed yet, ensure we try to setup when a markdown buffer is opened
      if not pcall(require, "obsidian") then
        vim.api.nvim_create_autocmd("FileType", {
          pattern = { "markdown" },
          callback = function()
            pcall(setup_obsidian, current_vault)
          end,
        })
      end
    end,
  }
}

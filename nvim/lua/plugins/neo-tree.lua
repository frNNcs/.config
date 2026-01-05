return {
    "nvim-neo-tree/neo-tree.nvim",
    branch = "v3.x",
    dependencies = {
        "nvim-lua/plenary.nvim",
        "nvim-tree/nvim-web-devicons",
        "MunifTanjim/nui.nvim",
    },
    config = function()
        require("neo-tree").setup({
            close_if_last_window = false,
            popup_border_style = "rounded",
            enable_git_status = true,
            enable_diagnostics = true,
            default_component_configs = {
                indent = { padding = 0 },
            },
            filesystem = {
                follow_current_file = true,
                use_libuv_file_watcher = true,
                hijack_netrw_behavior = "open_default",
                filtered_items = { visible = true },
            },
            window = { position = "right", width = 35 },
        })

        -- Keymap: leader+e para alternar
        vim.keymap.set("n", "<leader>e", function()
            require("neo-tree.command").execute({ toggle = true, dir = vim.loop.cwd() })
        end, { desc = "Toggle Neo-tree" })
    end,
}

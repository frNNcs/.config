return {
  {
    "nvim-treesitter/nvim-treesitter",
    opts = function(_, opts)
      if type(opts.ensure_installed) == "table" then
        vim.list_extend(opts.ensure_installed, { "typescript", "tsx", "javascript" })
      end
    end,
  },
  {
    "neovim/nvim-lspconfig",
    config = function()
      -- Neovim 0.11+ native LSP configuration
      -- Define configs (defaults)
      vim.lsp.config.ts_ls = {}
      vim.lsp.config.eslint = {}

      -- Enable servers
      vim.lsp.enable("ts_ls")
      vim.lsp.enable("eslint")
    end,
  },
}
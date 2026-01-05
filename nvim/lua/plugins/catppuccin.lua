return {
    'catppuccin/nvim',
    name = 'catppuccin',
    priority = 1000,
    config = function()
        require('catppuccin').setup({
            flavour = 'mocha',
            integrations = {
                treesitter = true,
                notify = true,
                nvimtree = true,
                telescope = true,
                which_key = true,
            },
        })
        vim.cmd('colorscheme catppuccin')
    end,
}
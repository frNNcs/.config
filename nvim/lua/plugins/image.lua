return {
  "samodostal/image.nvim",  -- Fork que funciona mejor con iTerm2
  ft = { "markdown" },
  dependencies = {
    "nvim-lua/plenary.nvim",
  },
  config = function()
    require("image").setup({
      render = {
        min_padding = 5,
        show_label = true,
        use_dither = true,
        foreground_color = false,
        background_color = false
      },
      events = {
        update_on_nvim_resize = true,
      },
    })
  end,
}

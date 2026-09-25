return {
  "romus204/tree-sitter-manager.nvim",
  dependencies = {},
  config = function()
    require("tree-sitter-manager").setup({
      auto_install = true, -- Automatically installs missing parsers when opening files!
      ensure_installed = { "bash", "python", "go", "lua", "vim", "vimdoc", "query", "markdown" }, 
    })
  end,
}

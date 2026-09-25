-- leader key
vim.g.mapleader = " "

-- normal keybinds
vim.keymap.set("n", "<leader>cd", vim.cmd.Ex)
vim.keymap.set("n", "<leader>wq", vim.cmd.wq)
vim.keymap.set("n", "<leader>so", vim.cmd.so)
vim.keymap.set("n", "<leader>bp", vim.cmd.bp)
vim.keymap.set("n", "<leader>bn", vim.cmd.bn)
vim.keymap.set("n", "[d", vim.diagnostic.goto_prev, opts)
vim.keymap.set("n", "]d", vim.diagnostic.goto_next, opts)
vim.keymap.set("n", "<leader>e", vim.diagnostic.open_float, opts)
vim.keymap.set("n", "<leader>q", vim.diagnostic.setloclist, opts)
vim.keymap.set('n', '<C-w>s', '<C-w>v', { desc = 'Split window vertically' })
vim.keymap.set('n', '<C-w>S', '<C-w>v', { desc = 'Split window vertically'})

-- visual mode
vim.keymap.set("v", "*", [[y/<C-R>"<CR>]], { desc = "Search highlighted text" })
vim.keymap.set("v", "p", '"_dP', { desc = "Paste without overwriting register" })
vim.keymap.set("v", "J", ":m '>+1<CR>gv=gv", { desc = "Move selection down" })
vim.keymap.set("v", "K", ":m '<-2<CR>gv=gv", { desc = "Move selection up" })
vim.keymap.set("v", '<Leader>c', "gU", { desc = "Capitalize selected text" })

-- instert mode
vim.keymap.set('i', '<C-u>', '<Esc>gUiwgi', { desc = 'Capitalize word under cursor' })

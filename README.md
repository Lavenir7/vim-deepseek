# vim-deepseek

## Dependency

```sh
sudo pip install openai pyyaml
```

## Installation

```vim
Plug 'Lavenir7/vim-deepseek'
```

## Storing API key

```vim
let g:deepseek_api_key = 'your-api-key'
```

## Key Mappings

```vim
" Chat with deepseek **once** with the content under the cursor
noremap <silent> <LEADER>aI :<C-U>call RunDeepSeekAsk()<CR>
" Chat with deepseek with the content under the cursor
noremap <silent> <LEADER>ai :<C-U>call RunDeepSeekChat()<CR>
" List all sessions
noremap <silent> <LEADER>al :<C-U>call ListChatSession()<CR>
" Select a session
noremap <silent> <LEADER>as :<C-U>call SetChatSession()<CR>
" Delete current session
noremap <silent> <LEADER>ad :<C-U>call DelChatSession()<CR>
" Clear session list
noremap <silent> <LEADER>aC :<C-U>call CleanChatSession()<CR>
```


## TODO

- [ ] 放一个轻量python包方便用户使用
- [ ] ListChatSession() 在光标附近生成窗口展示列表
- [ ] 支持调用Ollama部署的本地大模型，可以选择模型
- [ ] 支持一键将AI输出结果拉取到光标处 (insert mode, normal mode)
- [ ] CleanChatSession() 可全部清空（目前至少留存一个session）
- [ ] 在退出 vim 时自动清空所有 session（作为可选功能）
- [ ] 可以给 session 添加备注名称
- [ ] 脱离 python，使用 curl，bash、lua脚本，提高运行速度


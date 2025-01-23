# vim-deepseek

## 依赖库

```sh
sudo pip install openai pyyaml
```
> 说明
> 使用 `.yaml` 文件用于存储对话历史，让历史记录有更好的可读性。

## 安装

### 使用 vimplug 安装

在你的 `vim` 配置文件中添加该行：

```vim
Plug 'Lavenir7/vim-deepseek'
```

## 必要的配置

在你的 `vim` 配置文件中添加以下内容：

```vim
let g:deepseek_api_key = 'your-api-key' " 添加你的API key
let g:deepseek_model = 'dsV3' " 使用deepseek-V3模型
let g:deepseek_model = 'dsR1' " 使用deepseek-R1模型
```

## 键位说明

> [!tip]
> `vim-deepseek` 使用你光标下的内容作为输入

```vim
" <LEADER>aI : 单次询问（没有上下文）
noremap <silent> <LEADER>aI :<C-U>call RunDeepSeekAsk()<CR>
" <LEADER>ai : 连续对话
noremap <silent> <LEADER>ai :<C-U>call RunDeepSeekChat()<CR>
" <LEADER>al : 查看会话列表
noremap <silent> <LEADER>al :<C-U>call ListChatSession()<CR>
" <LEADER>as : 选择一个会话或创建一个新会话
noremap <silent> <LEADER>as :<C-U>call SetChatSession()<CR>
" <LEADER>ad : 删除当前会话
noremap <silent> <LEADER>ad :<C-U>call DelChatSession()<CR>
" <LEADER>aC : 清空会话列表
noremap <silent> <LEADER>aC :<C-U>call CleanChatSession()<CR>
```


## TODO

- [ ] 放一个轻量python包方便用户使用
- [x] 更新 DeepSeek-R1 模型
- [ ] ListChatSession() 在光标附近生成窗口展示列表
- [ ] 支持调用Ollama部署的本地大模型，可以选择模型
- [ ] 支持一键将AI输出结果拉取到光标处 (insert mode, normal mode)
- [ ] CleanChatSession() 可全部清空（目前至少留存一个session）
- [ ] 在退出 vim 时自动清空所有 session（作为可选功能）
- [ ] 可以给 session 添加备注名称
- [ ] 脱离 python，使用 curl，bash、lua脚本，提高运行速度


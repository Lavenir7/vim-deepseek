" ==================
" FileName: deepseek.vim
" Author: Lavenir7 <zzy0358e@163.com>
" GitHub: https://github.com/Lavenir7
" ==================

set encoding=utf-8
set fileencoding=utf-8
let s:ask_py_path = expand('<sfile>:p:h') . '/../script/ask.py'
let s:python_e = 'python'

function! RunDeepSeekAsk()
    let l:info = getcontent#GetContent()
    normal! v
    if l:info == ''
        echo 'No text selected.'
        return
    endif
    let l:cmd = python_e . ' ' . s:ask_py_path . ' -k ' . g:deepseek_api_key . ' ' . shellescape(l:info, 1)
    silent! execute 'terminal' l:cmd
    wincmd K
    wincmd w
endfunction


noremap <silent> <LEADER>aI :<C-U>call RunDeepSeekAsk()<CR>


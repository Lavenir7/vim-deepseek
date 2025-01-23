" ==================
" FileName: deepseek.vim
" Author: Lavenir7 <zzy0358e@163.com>
" GitHub: https://github.com/Lavenir7
" ==================

set encoding=utf-8
set fileencoding=utf-8
let s:python_e = 'python'
let s:init_py_path = expand('<sfile>:p:h') . '/../script/init.py'
let s:list_py_path = expand('<sfile>:p:h') . '/../script/list.py'
let s:chat_py_path = expand('<sfile>:p:h') . '/../script/chat.py'
let s:del_py_path = expand('<sfile>:p:h') . '/../script/delete.py'


function! s:InitChatSession(session_id)
    let l:cmd_init = s:python_e . ' ' . s:init_py_path . ' ' . a:session_id . ' &'
    call system(l:cmd_init)
endfunction

function! ListChatSession()
    let l:cmd_list = s:python_e . ' ' . s:list_py_path . ' -i ' . s:chat_session
    execute 'terminal' l:cmd_list
endfunction

function! RunDeepSeekChat()
    let l:info = getcontent#GetContent()
    normal! v
    if l:info == ''
        echohl ErrorMsg
        echo '[vim-deepseek] No text selected.'
        echohl None
        return
    endif
    let l:cmd = s:python_e . ' ' . s:chat_py_path . ' -k ' . g:deepseek_api_key . ' -m ' . g:deepseek_model . ' -s ' . s:chat_session . ' ' . shellescape(l:info, 1)
    silent! execute 'terminal' l:cmd
    wincmd K
    wincmd w
endfunction

function! SetChatSession()
    echohl MoreMsg
    let l:select_session = input("Please enter a session id: ")
    echohl None
    if l:select_session =~ '^\d\+$'
        let s:chat_session = l:select_session
        if index(s:chat_session_list, s:chat_session) == -1
            call add(s:chat_session_list, s:chat_session)
            call s:InitChatSession(s:chat_session)
            echohl ModeMsg
            echo "\nnew session: " . s:chat_session
            echohl None
        else
            " move to the tail
            let l:chat_session_index = index(s:chat_session_list, s:chat_session)
            call remove(s:chat_session_list, l:chat_session_index)
            call add(s:chat_session_list, s:chat_session)
            echohl ModeMsg
            echo "\nset session: " . s:chat_session
            echohl None
        endif
    else
        echohl ErrorMsg
        echo "\nshould enter a session id"
        echohl None
    endif
endfunction

function! DelChatSession(session_id_tmp = '-1', silent = 0)
    if a:session_id_tmp == '-1'
        let l:session_id = s:chat_session
    else
        let l:session_id = a:session_id_tmp
    endif
    let l:session_index = index(s:chat_session_list, l:session_id)
    if len(s:chat_session_list) == 1
        if a:silent == 0
            echohl ErrorMsg
            echo "Can't delete: only one session ( " . s:chat_session_list[0] . " )"
            echohl None
        endif
        return
    elseif l:session_index == -1
        if a:silent == 0
            echohl ErrorMsg
            echo "Doesn't exist session: " . l:session_id
            echohl None
        endif
        return
    else
        call remove(s:chat_session_list, l:session_index)
        let l:cmd_del = s:python_e . ' ' . s:del_py_path . ' ' . l:session_id
        call system(l:cmd_del)
        if a:silent == 0
            echohl WarningMsg
            echo "delete session: " . l:session_id
            echohl None
        endif
        if s:chat_session == l:session_id
            let s:chat_session = s:chat_session_list[-1]
        endif
    endif
endfunction

function! CleanChatSession()
    for exist_session in s:chat_session_list
        call DelChatSession(exist_session, 1)
    endfor
    echohl WarningMsg
    echo "The session list has been cleaned, except [" . s:chat_session . "]"
    echohl None
endfunction


function! s:Init()
    let s:chat_session = '0'
    let s:chat_session_list = []
    call s:InitChatSession(s:chat_session)
    let l:cmd_list0 = s:python_e . ' ' . s:list_py_path . ' -m 0'
    let l:exist_sessions = system(cmd_list0)
    if v:shell_error != 0
        echoerr "[vim-deepseek] init script failed"
        return
    endif
    let l:exist_session_list = split(l:exist_sessions, '\s\+')
    for exist_session_id in l:exist_session_list
        call add(s:chat_session_list, exist_session_id)
    endfor
endfunction

call s:Init()

noremap <silent> <LEADER>ai :<C-U>call RunDeepSeekChat()<CR>
noremap <silent> <LEADER>al :<C-U>call ListChatSession()<CR>
noremap <silent> <LEADER>as :<C-U>call SetChatSession()<CR>
noremap <silent> <LEADER>ad :<C-U>call DelChatSession()<CR>
noremap <silent> <LEADER>aC :<C-U>call CleanChatSession()<CR>


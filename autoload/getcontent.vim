" ==================
" FileName: deepseek.vim
" Author: Lavenir7 <zzy0358e@163.com>
" GitHub: https://github.com/Lavenir7
" ==================

function! s:GetCurrentContent()
    let l:current_mode = mode()
    if l:current_mode == 'i'
        " insert mode
        return ''
    elseif l:current_mode =~ 'v\|V\|\\22'
        " visual mode
        let l:old_v_reg = @v
        normal gv"vy
        let l:visual_content = @v
        let @v = l:old_v_reg
        return l:visual_content
    elseif l:current_mode == 'n'
        " normal mode
        let l:current_word = expand("<cWORD>")
        return l:current_word
    endif
endfunction

function! getcontent#GetContent()
    return s:GetCurrentContent()
endfunction


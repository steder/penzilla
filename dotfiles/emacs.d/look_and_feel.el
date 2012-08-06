;;; look_and_feel.el
;;
;; Sensible defaults for python
;; and general programming
(setq default-tab-width 4);
(global-font-lock-mode t);
(setq font-lock-maximum-decoration t);
(transient-mark-mode t);
(column-number-mode);
(size-indication-mode);

;;; the startup screen just slows things down:
(setq inhibit-startup-message t)

;;; higlight changes in documents
;; (global-highlight-changes-mode t)
;; (setq highlight-changes-visibility-initial-state nil); initially hide
;; ;; toggle visibility
;; (global-set-key (kbd "<f7>")      'highlight-changes-visible-mode) ;; changes
;; ;; remove the change-highlight in region
;; (global-set-key (kbd "S-<f7>")    'highlight-changes-remove-highlight)
;; ;; alt-pgup/pgdown jump to the previous/next changehello
;; ;; if you're not already using it for something else...
;; (global-set-key (kbd "<M-prior>") 'highlight-changes-next-change)
;; (global-set-key (kbd "<M-next>")  'highlight-changes-previous-change)
;; (set-face-foreground 'highlight-changes nil)
;; (set-face-background 'highlight-changes "#382f2f")
;; (set-face-foreground 'highlight-changes-delete nil)
;; (set-face-background 'highlight-changes-delete "#916868")

;;; highlight parens:
(setq show-paren-delay 0)
(show-paren-mode t)
;; show-paren-style can be:
; 'expression, 'parenthesis, 'mixed
; where mixed means highlight the
; whole expression only when the matching
; paren is not visible on screen
(setq show-paren-style 'mixed)
;; to customize styles for matches:
; (set-face-background 'show-paren-match-face "#aaaaaa")
; (set-face-attribute 'show-paren-match-face nil 
;         :weight 'bold :underline nil :overline nil :slant 'normal)
;; to customize style for mis-matches:
; (set-face-foreground 'show-paren-mismatch-face "red") 
; (set-face-attribute 'show-paren-mismatch-face nil 
;                     :weight 'bold :underline t :overline nil :slant 'normal)

;;; Disable some UI elements.
(if (fboundp 'tool-bar-mode) (tool-bar-mode -1))
;(if (fboundp 'menu-bar-mode) (menu-bar-mode -1))

;;; put the scrollbar on the right:
;; 'left is the default, 'right and nil are options
;; nil hides the scrollbar completely
(set-scroll-bar-mode 'right)

;;; Configure scrolling behavior:
;; scroll-margin: the cursors distance from the top/bottom when
;;  scrolling is triggered
;; scroll-conservatively: how far the cursor can be from the center of
;;  the screen when scrolling starts, 0 is the default and that causes
;;  the cursor to always jump to the center
;; scroll-preserve-screen-position: when on this tells emacs to the cursor
;;  in the same position on the screen as it scrolls
(setq
 scroll-margin 0
 scroll-conservatively 1000 
 scroll-preserve-screen-position 1)

;;visual bell instead of annoying beep
(setq visible-bell t)

;; Replace tabs with spaces
;;(setq indent-tabs-mode nil);
(setq-default indent-tabs-mode nil);

;;;  Fix backspace on textmode terminals
(if window-system
    ( normal-erase-is-backspace-mode 1 ) ;  if gui
    ( normal-erase-is-backspace-mode 0  )); if terminal

;; Narrow to region allows you to focus on a subset of a file
(put 'narrow-to-region 'disabled nil)
(put 'narrow-to-page 'disabled nil)

;; Save place in a file and open to that place when I reopen that file:
(require 'saveplace)
(setq-default save-place t);

;;; Tabbar! ^_^
(require 'tabbar)
;; customize tabbar styles:
(set-face-attribute
 'tabbar-default-face nil
 :background "gray60")
(set-face-attribute
 'tabbar-unselected-face nil
 :background "black"
 :foreground "gray85"
 :box nil)
(set-face-attribute
 'tabbar-selected-face nil
 :background "gray85"
 :foreground "black"
 :box nil)
(set-face-attribute
 'tabbar-button-face nil
 :box '(:line-width 1 :color "gray72" :style released-button))
(set-face-attribute
 'tabbar-separator-face nil
 :height 0.7)
;; 
(tabbar-mode)
(global-set-key [(control f10)] 'tabbar-local-mode)
(global-set-key [(control shift tab)] 'tabbar-backward)
(global-set-key [(control tab)]       'tabbar-forward)

;;; COLOR THEMES
(require 'color-theme)
(require 'color-theme-tango)
; (color-theme-comidia)
(if window-system
    (progn 
      (color-theme-initialize) ; If gui window, load this theme
      ( color-theme-tango )))
;  ( color-theme-euphoria )); If terminal, load this theme

;; Show the time on the status bar.
(display-time)

;; IDO mode, improved buffer switching
(require 'ido)
(ido-mode t)
(setq ido-enable-flex-matching t) ; fuzzy matching is a must have
(setq ido-use-filename-at-point t)
;; use normal find-file function for ftp files
(setq ido-slow-ftp-host-regexps '(".*"))
;; don't search files in other directories
(setq ido-work-directory-list-ignore-regexps '(".*"))

(put 'set-goal-column 'disabled nil)

;; just tell emacs to not bother prompting about loading / setting
;; local variables
;; :all, set all the variables and do not query
;; :safe, set only 'safe' variables and do not query
;; t, default, set safe variables and query
;; nil, don't set any variables
(setq enable-local-variables :all)
;(setq enable-local-eval t)

; customize find-grep to exclude vcs files:
(cond (linux-p
       (setq grep-find-command 
             "find . -type f '!' -wholename '*/.svn/*' -print0 | xargs -0 -e grep -nHi -e ")
       )
      ;; xargs on mac os x doesn't support -e option
      (macosx-p
       (setq grep-find-command 
             "find . -type f '!' -wholename '*/.svn/*' -print0 | xargs -0 grep -nHi -e ")
       )
      )


;; On write, delete trailing whitespace:
;(add-hook 'write-file-functions 'delete-trailing-whitespace)

;;; Quick hack to display tab characters:
;(standard-display-ascii ?\t "^I")

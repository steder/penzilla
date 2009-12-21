;; keybindings.el
;; defines a bunch of custom shortcuts
;;
; C-x-1: deletes all windows but current
; C-x-2: splits window vertically
; C-x-3: splits window horizontally
; C-x-0: deletes current window


;;;  Enable clipboard functions for copy and paste:
(setq x-select-enable-clipboard t)

(global-set-key "\C-cc\C-c" 'clipboard-kill-ring-save)
(global-set-key "\C-cc\C-x" 'clipboard-kill-region)
(global-set-key "\C-cc\C-v" 'clipboard-yank)

(global-set-key "\C-x\C-m" 'execute-extended-command)
(global-set-key "\C-c\C-m" 'execute-extended-command)

(global-set-key (kbd "RET") 'newline-and-indent)

; Search that should cross whitespace (newlines and the like)
;(global-set-key "" 'search-whitespace-regexp)
(global-set-key "\M-g" 'goto-line)
(global-set-key "\M-s" 'find-grep)
(global-set-key "\C-\M-s" 'find-grep-dired)

(global-set-key (kbd "C-5") 'query-replace)
(global-set-key (kbd "M-5") 'query-replace-regexp)

(global-set-key (kbd "M-`") 'next-error)
(global-set-key (kbd "C-`") 'previous-error)
; occur mode offers a "hypertext index" for a given buffer based on a given search criteria
(global-set-key (kbd "C-c o") 'occur)

;(require 'browse-kill-ring)
;(browse-kill-ring-default-keybindings)

;; Org Mode:
(add-to-list 'auto-mode-alist '("\\.org\\'" . org-mode))
(global-set-key "\C-cl" 'org-store-link)
(global-set-key "\C-ca" 'org-agenda)
(global-set-key "\C-cb" 'org-iswitchb)

;; http://emacs-fu.blogspot.com/2008/12/showing-line-numbers.html
(when (require 'linum)
  (global-set-key (kbd "<f6>") 'linum-mode))

;; from http://emacs-fu.blogspot.com/2009/02/transparent-emacs.html
(defun djcb-opacity-modify (&optional dec)
  "modify the transparency of the emacs frame; if DEC is t,
    decrease the transparency, otherwise increase it in 10%-steps"
  (let* ((alpha-or-nil (frame-parameter nil 'alpha)) ; nil before setting
          (oldalpha (if alpha-or-nil alpha-or-nil 100))
          (newalpha (if dec (- oldalpha 10) (+ oldalpha 10))))
    (when (and (>= newalpha frame-alpha-lower-limit) (<= newalpha 100))
      (modify-frame-parameters nil (list (cons 'alpha newalpha))))))

;; C-8 will increase opacity (== decrease transparency)
;; C-9 will decrease opacity (== increase transparency
;; C-0 will returns the state to normal
(global-set-key (kbd "C-8") '(lambda()(interactive)(djcb-opacity-modify)))
(global-set-key (kbd "C-9") '(lambda()(interactive)(djcb-opacity-modify t)))
(global-set-key (kbd "C-0") '(lambda()(interactive)
                               (modify-frame-parameters nil `((alpha . 100)))))

;; Another emacs-fu snippet:
(defun djcb-zoom (n)
  "with positive N, increase the font size, otherwise decrease it"
  (set-face-attribute 'default (selected-frame) :height 
    (+ (face-attribute 'default :height) (* (if (> n 0) 1 -1) 10)))) 

(global-set-key (kbd "C-+")      '(lambda nil (interactive) (djcb-zoom 1)))
(global-set-key [C-kp-add]       '(lambda nil (interactive) (djcb-zoom 1)))
(global-set-key (kbd "C--")      '(lambda nil (interactive) (djcb-zoom -1)))
(global-set-key [C-kp-subtract]  '(lambda nil (interactive) (djcb-zoom -1)))

;;; Just a bunch of modes that I'm trying.
;;; These can sit in misc.el because
;;; they made not last long.

;; Load version control module
(require 'vc)
(setq ;; Always follow links if the file is under version control
 vc-follow-symlinks t
    )

;; JIRA!
(require 'jira)
(setq jira-url "http://jira.texturallc.net:8080/rpc/xmlrpc")

;; Desktop Module
;;(desktop-save-mode 1)

;; js2-mode by Steve Yegge
(autoload 'js2-mode "js2" nil t)
(add-to-list 'auto-mode-alist '("\\.js$" . js2-mode))

;; GraphViz mode:
(load-file "~/etc/emacs.d/graphviz-dot-mode.el")

;; Midnight Mode?  ClearBufferList?
(require 'midnight)

;; GO MODE:
;; To install go-mode, add the following lines to your .emacs file:
;(add-to-list 'load-path "PATH CONTAINING go-mode-load.el" t)
(require 'go-mode-load)
;; After this, go-mode will be used for files ending in '.go'.

;; Undo-tree mode:
; This mode provides a visualization
; of the tree of undo state provided by emacs.
(require 'undo-tree)
(global-undo-tree-mode)



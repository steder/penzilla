;;;  LOOK AND FEEL
;(custom-set-faces
; '(my-tab-face            ((((class color)) (:background "grey10"))) t)
; '(my-trailing-space-face ((((class color)) (:background "gray10"))) t)
; '(my-long-line-face ((((class color)) (:background "gray10"))) t))

;; (add-hook 'font-lock-mode-hook
;;           (function
;;            (lambda ()
;;              (setq font-lock-keywords
;;                    (append font-lock-keywords
;;                            '(("\t+" (0 'my-tab-face t))
;;                              ("^.\\{81,\\}$" (0 'my-long-line-face t))
;;                              ("[ \t]+$"      (0 'my-trailing-space-face t))))))))

;; Emacs Generated config:
(custom-set-variables
  ;; custom-set-variables was added by Custom.
  ;; If you edit it by hand, you could mess it up, so be careful.
  ;; Your init file should contain only one such instance.
  ;; If there is more than one, they won't work right.
 '(c-default-style (quote ((java-mode . "java") (awk-mode . "awk") (other . "stroustrup"))))
 '(org-agenda-files (quote ("~/bugs/test.org")))
 '(uniquify-buffer-name-style (\` reverse) nil (uniquify)))

(custom-set-faces
  ;; custom-set-faces was added by Custom.
  ;; If you edit it by hand, you could mess it up, so be careful.
  ;; Your init file should contain only one such instance.
  ;; If there is more than one, they won't work right.
 )


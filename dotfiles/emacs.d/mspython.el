;; Advanced Python stuff
;; Pymacs
;(require 'pymacs)
;(autoload 'pymacs "pymacs" nil t)
;(autoload 'pymacs-load "pymacs" nil t)
;(autoload 'pymacs-eval "pymacs" nil t)
;(autoload 'pymacs-apply "pymacs")
;(autoload 'pymacs-call "pymacs")

;; python-mode:
;(setq load-path (cons "/usr/share/emacs/site-lisp" load-path))
(autoload 'python-mode "python-mode" "Python editing mode." t)
;(setq auto-mode-alist
;      (cons '("\\.py$" . python-mode) auto-mode-alist))

;; Bicycle Repair - Python Refactoring
;(pymacs-load "bikeemacs" "brm-")
;(brm-init)

;; PYTHON MODE FOR TWISTED
(add-to-list 'auto-mode-alist '("\\.tap\\'" . python-mode))
(add-to-list 'auto-mode-alist '("\\.tac\\'" . python-mode))
(add-to-list 'auto-mode-alist '("\\.tml\\'" . python-mode))

;; Pyflakes and Flymake for Python!  WHOOO!
; (defun py-pychecker-run ()
;  (interactive)
;    (shell-command (concat
;                    "pyflakes "
;                    (buffer-file-name))
;                   "*compilation*")
;    (switch-to-buffer-other-window "*compilation*"))

;; configure hooks to run pyflakes automatically with flymake mode:
;; NOTE: this is super sweet
(when (load "flymake" t)
  (defun flymake-pyflakes-init ()
    (let* ((temp-file (flymake-init-create-temp-buffer-copy
                       ;'flymake-create-temp-inplace))
                       'flymake-create-temp-with-folder-structure))
           (local-file (file-relative-name
                        temp-file
                        (file-name-directory buffer-file-name))))
      (list "pyflakes" (list local-file))))
  (delete '("\\.html?\\'" flymake-xml-init) flymake-allowed-file-name-masks)
  (add-to-list 'flymake-allowed-file-name-masks
               '("\\.py\\'" flymake-pyflakes-init)))

(add-hook 'find-file-hook 'flymake-find-file-hook)

;; run pyflakes(instead of pychecker) manually with C-c C-w:
(setq py-pychecker-command "pyflakes")
(setq py-pychecker-command-args "")

;; MS TEST
(require 'mstest)

;; YAML mode:
(require 'yaml-mode)
(add-to-list 'auto-mode-alist '("\\.yml$" . yaml-mode))

;; Let's try treating psp files as xml?
(add-to-list 'auto-mode-alist '("\\.psp\\'" . nxml-mode))
;;(add-to-list 'auto-mode-alist '("\\.jsp\\'" . jsp-mode))


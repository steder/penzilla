;;; mstest.el

;;; Dependencies:

;; This module depends on msproject.el

(provide 'mstest)

(defvar test-case-name nil "Hello")
(make-variable-buffer-local 'test-case-name)
(defconst path-seperator "/")

(defun show-test-case-name ()
  (interactive)
  (message (format "%s" test-case-name)))

(defun get-test-case-name ()
  (if test-case-name
      test-case-name
      buffer-file-name
    )
  )

(defun mstest-runtest ()
  (interactive)
  (hack-local-variables)
  (compile (format "cd %s; nose.py %s"
                   (msproject-project-root)
                   (get-test-case-name))
           )
)

(define-minor-mode mstest-mode
  "toggle mstest mode.
   with no argument toggles
   with non-null prefix turns on mode
   with null prefix turns off the mode."
  ;; initial value
  nil
  ;; indicator for mode line:
  " mstest"
  ;; minor mode keybindings:
  '(
    ([f9] . mstest-runtest)
    )
  )

(add-hook
 'python-mode-hook
 (lambda ()
   (mstest-mode t)))

;;; msproject.el

;; About:

;; This module describes project-wide functionality
;; for Textura projects and others.

;;; Ideas for functionality:

;; 1. find-in-project to recursively grep from the project root down
;; independent of where the grep started.
;; 2. ...
;; ?. Build and locate TAGS files?

(defvar msproject-root-files
  '("tconsole.py"
    )
  "File(s) that identify the project rool"
  )

;; Depending on the type of project
;; we may use one of many possible files
;; as the project root.
;;
;; For example:
;;   - CPM: tconsole.py
;;   - arbitrary django project: manage.py
;;   - arbitrary twisted project: twisted (twisted plugin directory?)

(defun msproject-project-root-helper (filename remaining)
  (locate-dominating-file (if buffer-file-name buffer-file-name ".") filename)
  )

(defun msproject-project-root ()
  (let (root)
    (setq root
          (msproject-project-root-helper
           (car msproject-root-files)
           (cdr msproject-root-files)
           )
          )
    (if (eq root nil)
        "."
      root)
    )
  )

(defun msproject-show-project-root ()
  (interactive)
  (message "project-root: %s" (msproject-project-root))
  )

;; (defun find-in-project (regexp files)
;;   "Simply runs rgrep starting from the project root directory"
;;   (interactive (list
;;                 (read-regexp "Search for(regexp)") 
;;                 (read-regexp "Search files matching regexp:" "*.py")
;;                 )
;;                )
;;   (message "args: %s, %s, %s" regexp files (msproject-project-root))
;;   (rgrep regexp files (msproject-project-root))
;;   )

;; ;; looks like find-in-project would work if this rgrep would work.
;; (rgrep "hello" "*.py" ".")

(defun msproject-grep-find-command ()
  "modifies grep-find-command to point at the root directory"
  (combine-and-quote-strings (cons "find" (cons (msproject-project-root) (cdr (cdr (split-string grep-find-command))))))
  )

(defun find-in-project (command-args)
  "Run grep via find, with user-specified args COMMAND-ARGS.
Collect output in a buffer.
While find runs asynchronously, you can use the \\[next-error] command
to find the text that grep hits refer to.

This command uses a special history list for its arguments, so you can
easily repeat a find command."
  (interactive
   (progn
     (grep-compute-defaults)
     (if grep-find-command
	 (list (read-shell-command "Run find (like this): "
                                   (msproject-grep-find-command) 'grep-find-history))
       ;; No default was set
       (read-string
        "compile.el: No `grep-find-command' command available. Press RET.")
       (list nil))))
  (when command-args
    (let ((null-device nil))		; see grep
      (grep command-args))))

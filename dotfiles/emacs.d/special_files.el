;;; special_files.el
;;
;; Here we have configurations for
;; all emacs features that create
;; files in the current directory
;; 
;; So instead of cluttering up
;; whatever directory you're in
;; with ~ backup files and so on
;; you can configure custom
;; locations for this stuff.
;;
;;; Keep backups stored in a central location:
(defvar backup-dir "~/.emacs.d/~backups")
(setq backup-directory-alist (list (cons "." backup-dir)))

;;; Keep bookmark files in a central location:
;; basic bookmark commands:
;; C-x r m (make a new bookmark defaulting to the current buffer/file)
;; C-x r b (jump to a bookmark)
;; C-x r l (list bookmarks)
(setq
 bookmark-default-file "~/.emacs.d/bookmarks"
 bookmark-save-flag 1) ;; autosave each change
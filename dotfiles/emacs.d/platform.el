;; See if we're on MS Windows or Mac OS X
(defvar mswindows-p (string-match "windows" (symbol-name system-type)))
(defvar macosx-p (string-match "darwin" (symbol-name system-type)))
(defvar linux-p (string-match "linux" (symbol-name system-type)))

;(if macosx-p
;    (progn
;      
;      )
;  )
(defun get-file ()
  (with-open-file (stream "outputs")
    (loop for line = (read-line stream nil)
          while line
          collect (parse-integer line))))

(defun write-numeric-list(l)
  (with-open-file (out "outputs" :direction :output :if-does-not-exist :create)
    (dolist (segment l)
      (format out "~D~C" segment #\newline))))

(defun add-num-all (list)
  (loop for e in list collect (1+ e)))


(write-numeric-list (add-num-all (get-file)))
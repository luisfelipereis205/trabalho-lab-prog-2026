#| O script em Common Lisp contendo funções puras sem efeitos colaterais para calcular a interseção de listas de amigos usando recursão, map, reduce ou filter. |#
;;;; ==========================================================================
;;;; MÓDULO FUNCIONAL - COMMON LISP (SBCL)
;;;; Projeto Integrado: Análise e Recomendação de Conexões em Redes Sociais
;;;; ==========================================================================

;;; 1. Verifica recursivamente se um elemento pertence a uma lista (Função Pura)
(defun pertence-p (elemento lista)
  (cond
    ((null lista) nil)
    ((equal elemento (car lista)) t)
    (t (pertence-p elemento (cdr lista)))))

;;; 2. Calcula a interseção entre duas listas usando RECURSÃO pura (sem alterar originais)
(defun intersecao-recursiva (lista-a lista-b)
  (cond
    ((null lista-a) nil)
    ((pertence-p (car lista-a) lista-b)
     (cons (car lista-a)
           (intersecao-recursiva (cdr lista-a) lista-b)))
    (t (intersecao-recursiva (cdr lista-a) lista-b))))

;;; 3. Calcula a interseção usando FILTER (remove-if-not)
(defun intersecao-filter (lista-a lista-b)
  (remove-if-not (lambda (amigo) (pertence-p amigo lista-b))
                 lista-a))

;;; 4. Conta elementos usando MAP (mapcar) e REDUCE
(defun contar-elementos (lista)
  (reduce #'+ (mapcar (lambda (x) (declare (ignore x)) 1) lista)
          :initial-value 0))

;;; 5. Calcula pontuação de afinidade (coeficiente de Jaccard)
(defun calcular-afinidade (lista-a lista-b)
  (let* ((comuns (intersecao-filter lista-a lista-b))
         (qtd-comuns (contar-elementos comuns))
         (total-a (contar-elementos lista-a))
         (total-b (contar-elementos lista-b))
         (uniao (- (+ total-a total-b) qtd-comuns)))
    (if (zerop uniao)
        0.0
        (float (/ qtd-comuns uniao)))))

;;; 6. Garante formato decimal JSON válido com ponto (ex: "0.50") independente do idioma
(defun formatar-decimal-json (numero)
  (substitute #\. #\, (format nil "~,2f" numero)))

;;; 7. Converte lista Lisp para array JSON: ["bruno", "eduardo"]
(defun lista-para-json (lista)
  (format nil "[~{~s~^, ~}]" lista))

;;; 8. Gera a resposta estruturada em JSON (Contrato de Dados com Python)
(defun gerar-resposta-json (usuario-origem candidato amigos-a amigos-b)
  (let* ((comuns (intersecao-recursiva amigos-a amigos-b))
         (qtd (contar-elementos comuns))
         (afinidade (formatar-decimal-json (calcular-afinidade amigos-a amigos-b))))
    (format nil "{\"usuario_origem\": ~s, \"candidato\": ~s, \"amigos_em_comum\": ~a, \"total_em_comum\": ~d, \"afinidade\": ~a}"
            usuario-origem
            candidato
            (lista-para-json comuns)
            qtd
            afinidade)))

;;; 9. Ponto de entrada: aceita argumentos do Python ou roda o caso de teste
(defun main ()
  (let ((args (cdr sb-ext:*posix-argv*)))
    (if (>= (length args) 4)
        ;; Quando chamado pelo Python:
        ;; sbcl --script lisp/intersecao.lisp "ana" "daniela" "bruno,carlos" "bruno,gabriel"
        (let ((origem (nth 0 args))
              (candidato (nth 1 args))
              (amigos-a (uiop:split-string (nth 2 args) :separator ","))
              (amigos-b (uiop:split-string (nth 3 args) :separator ",")))
          (format t "~a~%" (gerar-resposta-json origem candidato amigos-a amigos-b)))
        
        ;; Quando rodado sem argumentos (teste local ou no navegador):
        (let ((amigos-ana '("bruno" "carlos" "eduardo"))
              (amigos-daniela '("bruno" "gabriel" "eduardo")))
          (format t "~a~%" (gerar-resposta-json "ana" "daniela" amigos-ana amigos-daniela))))))

(main)
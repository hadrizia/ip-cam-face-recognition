# ip-cam-face-recognition

   O face-recognition é uma biblioteca open-source criada a partir da dlib com deep-learning. (Mais informações podem ser encontradas no link: http://face-recognition.readthedocs.io/en/latest/readme.html).

   Esta biblioteca foi testada através de um código que carrega e processa rostos de pessoas em formato .jpg e executa o reconhecimento entre os rostos cadastrados e os frames de uma streaming IP cam. Para executá-lo, basta rodar as seguintes linhas de comando:
   
```
   sudo apt-get install python-opencv
```
```
   sudo pip2 install face-recognition
```
```
python face-recognition.py
``` 
   A seguir serão descritos alguns aspectos observados sobre a biblioteca.

   * Pontos positivos
   		* Rapidez na detecção e reconhecimento dos rostos: O algoritmo se mostrou bastante eficaz na detecção e no reconhecimento das faces;
   		* Usabilidade: A biblioteca é simples, fácil de usar e bem documentada;
   		* Acurácia no reconhecimento: O modelo se comportou bem no reconhecimento, diferenciando inclusive rostos parecidos (rostos de irmãos);

   	* Limitações
   		* Baixo alcance de detecção: Para que a detecção ocorra, o indivíduo deve estar a uma curta distância da câmera;
         * Reconhecimento pode ser comprometido: Apesar de reconhecer uma pessoa ao usar capuz, óculos e/ou cabelo preso, ocultar a boca pode comprometer o reconhecimento.

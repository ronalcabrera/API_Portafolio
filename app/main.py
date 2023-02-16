from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get('/', response_class = HTMLResponse)
async def mensaje():
        return """
<!doctype html>
<html lang="en">
  <script async="false" type="text/javascript" src="chrome-extension://fnjhmkhhmkbjkkabndcnnogagogbneec/in-page.js"></script>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Números</title>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">

    <style>
      #resultado, #resultado2, #resultado3 {
        color:#ccc;
        font-weight:  bold;
        font-size:  6rem;
        text-align: center;
        display:  inline-block;
      }

      body {  
        background-color: #22272e;
        color:#ccc;
        font-family: verdana;
        font-size: 75%;
      }

      table {
        margin: 0 auto;
      }

      table, th, tr, td {
        border: 1px solid #ccc;
      }

      th {
        padding: 10px;
      }

      .canvas-container {
        margin: 0 auto;
        border: 1px solid #ccc;
        background-color: goldenrod;
      }
    </style>

  <script src="https://www.googletagmanager.com/gtag/js?l=dataLayer&amp;id=G-JMXEL2D511" async=""></script>
  </head>

  <body>    
    <main>
      <div class="px-4 py-2 my-2 text-center border-bottom">
        <h1 class="display-5 fw-bold">Números escritos a mano</h1>
        <div class="col-lg-6 mx-auto">
          <p class="lead mb-0">Predicción de números escritos a mano utilizando Tensorflow.js</p>
          <p class="lead mb-0">Para una mejor lectura utilice números grandes y centrados!!</p>
        </div>
      </div>

      <div class="b-example-divider"></div>

      <div class="container mt-5">
        <div class="row">
          <div class="col-12 col-md-4 offset-md-4">
            <div id="canvas-container">
              <canvas id="bigcanvas" width="200" height="200"></canvas>
              <canvas id="smallcanvas" width="28" height="28" style="display: none"></canvas>
            </div>
            <div class="text-center mt-3">
              <button class="btn btn-primary" id="limpiar" onclick="limpiar()">Limpiar</button>
              <button class="btn btn-success" id="predecir" onclick="predecir()">Predecir</button>
            </div>
            
          </div>
        </div>
        <div class="row">
          <div class="col-12 col-md-6 offset-md-3">
              <div class="mt-2 text-center">

                <table>
                  <thead>
                    <tr><th>Modelo denso</th>
                    <th>Modelo Convolucional</th>
                    <th>Modelo Convolucional c/aumemto de datos</th></tr>
                  </thead>                  
                  <tbody>
                    <tr>
                      <td><div id="resultado" class="resultado"></div></td>
                      <td><div id="resultado2" class="resultado"></div></td>
                      <td><div id="resultado3" class="resultado"></div></td>
                    </tr>
                  </tbody>                
                </table>              
              </div>
            </div>
          </div>
          <div class="col-lg-6 mx-auto">
            <br>
            <p>Como puede apreciarse, es muy importante el aumento de datos ya que le da mas flexibilidad al modelo</p>
            <p>El DROPOUT permite que el modelo tenga en cuenta todos los detalles a la hora de entrenar, no solo los pesos mas grandes.</p>
          </div>

        </div>
      </div>

      <div class="b-example-divider mb-0"></div>
    </main>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>

    <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@2.0.0/dist/tf.min.js"></script>
    <script src="fabric.min.js"></script>
    <script src="drawing.js"></script>

    <script type="text/javascript">

    var modelo = null;
    var modelo2 = null;
    var modelo3 = null;

      //Tomar y configurar el canvas
      var canvas = document.getElementById("bigcanvas");
      var ctx1 = canvas.getContext("2d");
      var smallcanvas = document.getElementById("smallcanvas");
      var ctx2= smallcanvas.getContext("2d");

      function limpiar() {
          ctx1.clearRect(0, 0, canvas.width, canvas.height);
          drawingcanvas.clear();
      }

      function predecir() {
            //Pasar canvas a version 28x28
            resample_single(canvas, 28, 28, smallcanvas);

            var imgData = ctx2.getImageData(0,0,28,28);
            var arr = []; //El arreglo completo
            var arr28 = []; //Al llegar a 28 posiciones se pone en 'arr' como un nuevo indice
            for (var p=0, i=0; p < imgData.data.length; p+=4) {
                var valor = imgData.data[p+3]/255;
                arr28.push([valor]); //Agregar al arr28 y normalizar a 0-1. Aparte queda dentro de un arreglo en el indice 0... again
                if (arr28.length == 28) {
                    arr.push(arr28);
                    arr28 = [];
                }
            }

            arr = [arr];  //Meter el arreglo en otro arreglo por que debe estar en un arreglo nuevo en el indice 0
                          //por ser un tensor4d en forma 1, 28, 28, 1
            var tensor4 = tf.tensor4d(arr);

            //Modelo 1
            var resultados = modelo.predict(tensor4).dataSync();
            var mayorIndice = resultados.indexOf(Math.max.apply(null, resultados));
            console.log("Prediccion 1", mayorIndice);
            document.getElementById("resultado").innerHTML = mayorIndice;

            //Modelo 2
            var resultados = modelo2.predict(tensor4).dataSync();
            var mayorIndice = resultados.indexOf(Math.max.apply(null, resultados));
            console.log("Prediccion 2", mayorIndice);
            document.getElementById("resultado2").innerHTML = mayorIndice;

            //Modelo 3
            var resultados = modelo3.predict(tensor4).dataSync();
            var mayorIndice = resultados.indexOf(Math.max.apply(null, resultados));
            console.log("Prediccion 3", mayorIndice);
            document.getElementById("resultado3").innerHTML = mayorIndice;
        }

        /**
         * Hermite resize - fast image resize/resample using Hermite filter. 1 cpu version!
         * 
         * @param {HtmlElement} canvas
         * @param {int} width
         * @param {int} height
         * @param {boolean} resize_canvas if true, canvas will be resized. Optional.
         * Cambiado por RT, resize canvas ahora es donde se pone el chiqitillllllo
         */
        function resample_single(canvas, width, height, resize_canvas) {
            var width_source = canvas.width;
            var height_source = canvas.height;
            width = Math.round(width);
            height = Math.round(height);

            var ratio_w = width_source / width;
            var ratio_h = height_source / height;
            var ratio_w_half = Math.ceil(ratio_w / 2);
            var ratio_h_half = Math.ceil(ratio_h / 2);

            var ctx = canvas.getContext("2d");
            var ctx2 = resize_canvas.getContext("2d");
            var img = ctx.getImageData(0, 0, width_source, height_source);
            var img2 = ctx2.createImageData(width, height);
            var data = img.data;
            var data2 = img2.data;

            for (var j = 0; j < height; j++) {
                for (var i = 0; i < width; i++) {
                    var x2 = (i + j * width) * 4;
                    var weight = 0;
                    var weights = 0;
                    var weights_alpha = 0;
                    var gx_r = 0;
                    var gx_g = 0;
                    var gx_b = 0;
                    var gx_a = 0;
                    var center_y = (j + 0.5) * ratio_h;
                    var yy_start = Math.floor(j * ratio_h);
                    var yy_stop = Math.ceil((j + 1) * ratio_h);
                    for (var yy = yy_start; yy < yy_stop; yy++) {
                        var dy = Math.abs(center_y - (yy + 0.5)) / ratio_h_half;
                        var center_x = (i + 0.5) * ratio_w;
                        var w0 = dy * dy; //pre-calc part of w
                        var xx_start = Math.floor(i * ratio_w);
                        var xx_stop = Math.ceil((i + 1) * ratio_w);
                        for (var xx = xx_start; xx < xx_stop; xx++) {
                            var dx = Math.abs(center_x - (xx + 0.5)) / ratio_w_half;
                            var w = Math.sqrt(w0 + dx * dx);
                            if (w >= 1) {
                                //pixel too far
                                continue;
                            }
                            //hermite filter
                            weight = 2 * w * w * w - 3 * w * w + 1;
                            var pos_x = 4 * (xx + yy * width_source);
                            //alpha
                            gx_a += weight * data[pos_x + 3];
                            weights_alpha += weight;
                            //colors
                            if (data[pos_x + 3] < 255)
                                weight = weight * data[pos_x + 3] / 250;
                            gx_r += weight * data[pos_x];
                            gx_g += weight * data[pos_x + 1];
                            gx_b += weight * data[pos_x + 2];
                            weights += weight;
                        }
                    }
                    data2[x2] = gx_r / weights;
                    data2[x2 + 1] = gx_g / weights;
                    data2[x2 + 2] = gx_b / weights;
                    data2[x2 + 3] = gx_a / weights_alpha;
                }
            }

            //Ya que esta, exagerarlo. Blancos blancos y negros negros..?

            for (var p=0; p < data2.length; p += 4) {
                var gris = data2[p]; //Esta en blanco y negro

                if (gris < 100) {
                    gris = 0; //exagerarlo
                } else {
                    gris = 255; //al infinito
                }

                data2[p] = gris;
                data2[p+1] = gris;
                data2[p+2] = gris;
            }


            ctx2.putImageData(img2, 0, 0);
        }

      //Cargar modelo
      (async () => {
        console.log("Cargando modelo 1...");
        modelo = await tf.loadLayersModel("https://github.com/ronalcabrera/ronalcabrera.github.io/blob/main/exportacion/modelo_denso/model.json");
        console.log("Modelo 1 cargado...");

        console.log("Cargando modelo 2...");
        modelo2 = await tf.loadLayersModel("https://github.com/ronalcabrera/ronalcabrera.github.io/blob/main/exportacion/modelo_CNN/model.json");
        console.log("Modelo 2 cargado...");

        console.log("Cargando modelo 3...");
        modelo3 = await tf.loadLayersModel("https://github.com/ronalcabrera/ronalcabrera.github.io/blob/main/exportacion/modelo_CNN_AD_DO/model.json");
        console.log("Modelo 3 cargado...");

    })();
    </script>
  </body>
</html>
"""                  
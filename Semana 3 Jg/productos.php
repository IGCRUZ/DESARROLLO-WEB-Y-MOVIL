<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PAGINA PRINCIPAL</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
</head>

<body>
    <!-- A grey horizontal navbar that becomes vertical on small screens -->
    <nav class="navbar navbar-expand-sm bg-secondary">

        <div class="container-fluid">
            <!-- Links -->
            <ul class="navbar-nav">
                <a class="navbar-brand" href="index.php"><i class="fa fa-android"></i></a>
                <li class="nav-item">
                    <a class="nav-link" href="contacto.php" style="color:white;">Contacto</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="empresa.php" style="color:white;">Empresa</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="productos.php" style="color:white;">Productos</a>
                </li>
            </ul>

            <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#myModal">
                <?xml version="1.0" ?><svg style="width: 20px; height: 20px;" viewBox="0 0 32 32"
                    xmlns="http://www.w3.org/2000/svg">
                    <title />
                    <g id="about">
                        <path d="M16,16A7,7,0,1,0,9,9,7,7,0,0,0,16,16ZM16,4a5,5,0,1,1-5,5A5,5,0,0,1,16,4Z" />
                        <path
                            d="M17,18H15A11,11,0,0,0,4,29a1,1,0,0,0,1,1H27a1,1,0,0,0,1-1A11,11,0,0,0,17,18ZM6.06,28A9,9,0,0,1,15,20h2a9,9,0,0,1,8.94,8Z" />
                    </g>
                </svg>
            </button>
        </div>

    </nav>


    <div class="container-fluid mt-3" style="background-color: lightblue;">
        <div class="row">

            <div class="col-12 col-sm-6 col-md-4 col-lg-3">
                <div class="card h-100">

                    <img class="card-img-top"
                        src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS5wSJi-Lz_0J5bfMlReQrlA04i3EB1uorr8YnsuieVPIUimQltIJSZyHU&s=10"
                        alt="Card image" style="width:100%; height:150px">

                    <div class="card-body d-flex flex-column">

                        <h4 id="producto1" class="card-title">
                            Balon Cuadrado
                        </h4>

                        <p class="card-text">
                            Perfecto para jugar en minecraft
                        </p>

                        <!-- ID AGREGADO PARA DOM -->
                        <a href="#" id="precio1" class="btn btn-primary mt-auto">
                            $10.000
                        </a>

                    </div>
                </div>
            </div>


            <div class="col-12 col-sm-6 col-md-4 col-lg-3">
                <div class="card h-100">

                    <img class="card-img-top"
                        src="https://i.pinimg.com/736x/03/d0/4b/03d04b611a7ecafe906ba9a4b77634bc.jpg"
                        alt="Card image"
                        style="width:100%; height:150px">

                    <div class="card-body d-flex flex-column">

                        <h4 id="producto2" class="card-title">
                            Nike Carton Flex 4
                        </h4>

                        <p class="card-text">
                            Zapatos perfecto para la combinacion con el balon cuadrado, nadie te
                            podra parar!
                        </p>

                        <!-- ID AGREGADO PARA DOM -->
                        <a href="#" id="precio2" class="btn btn-primary mt-auto">
                            $58.990
                        </a>

                    </div>
                </div>
            </div>


            <div class="col-12 col-sm-6 col-md-4 col-lg-3">
                <div class="card h-100">

                    <img class="card-img-top"
                        src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQk1kGY3cfp0heQS38wn0u1sN52PdV-YNbZKJVXZSftdw&s=10"
                        alt="Card image"
                        style="width:100%; height:150px">

                    <div class="card-body d-flex flex-column">

                        <h4 id="producto3" class="card-title">
                            Guantes chiquitos
                        </h4>

                        <p class="card-text">
                            Al puro estilo de el Friibu Martinez, Con estos guantes no se te pasa
                            ninguna
                        </p>

                        <!-- ID AGREGADO PARA DOM -->
                        <a href="#" id="precio3" class="btn btn-primary mt-auto">
                            $14.980
                        </a>

                    </div>
                </div>
            </div>


            <div class="col-12 col-sm-6 col-md-4 col-lg-3">
                <div class="card h-100">

                    <img class="card-img-top"
                        src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRi1BHyYsDayT15GahHRzseV7OujrRRcAbdg9lY7fYEBHySp6osi4IkDKU&s=10"
                        alt="Card image"
                        style="width:100%; height:150px">

                    <div class="card-body d-flex flex-column">

                        <h4 id="producto4" class="card-title">
                            Camiseta Aguante el Furbo
                        </h4>

                        <p class="card-text">
                            Con esta camiseta, ni tu novia se podra negar a un furbito
                        </p>

                        <!-- ID AGREGADO PARA DOM -->
                        <a href="#" id="precio4" class="btn btn-primary mt-auto">
                            $67.670
                        </a>

                    </div>
                </div>
            </div>

        </div>
    </div>


    <div class="modal fade" id="myModal">
        <div class="modal-dialog">
            <div class="modal-content">

                <!-- Modal Header -->
                <div class="modal-header">
                    <h4 class="modal-title">Ingreso de Usuarios</h4>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>

                <!-- Modal body -->
                <form action="acceso.php">
                    <div class="modal-body">

                        <div class="mb-3 mt-3">
                            <label for="email" class="form-label">Email:</label>
                            <input type="email" class="form-control" id="email" placeholder="Ingresar Email"
                                name="email">
                        </div>

                        <div class="mb-3">
                            <label for="pwd" class="form-label">Contraseña:</label>
                            <input type="password" class="form-control" id="pwd"
                                placeholder="Ingresar Contraseña" name="pswd">
                        </div>

                        <div class="form-check mb-3">
                            <label class="form-check-label">
                                <input class="form-check-input" type="checkbox" name="remember">
                                Recordar Contraseña
                            </label>
                        </div>

                    </div>

                    <!-- Modal footer -->
                    <div class="modal-footer">
                        <button type="submit" class="btn btn-primary" data-bs-dismiss="modal">
                            Acceder
                        </button>

                        <button type="button" class="btn btn-danger" data-bs-dismiss="modal">
                            Cerrar
                        </button>
                    </div>
                </form>

            </div>
        </div>
    </div>


    <!-- DOM + JAVASCRIPT -->
    <script>

        document.getElementById("precio1").onclick = function() {

            this.style.color = "green";
            this.style.fontWeight = "bold";

            alert("Producto seleccionado: " +
                document.getElementById("producto1").textContent +
                " - Precio: " +
                this.textContent);

        };


        document.getElementById("precio2").onclick = function() {

            this.style.color = "green";
            this.style.fontWeight = "bold";

            alert("Producto seleccionado: " +
                document.getElementById("producto2").textContent +
                " - Precio: " +
                this.textContent);

        };


        document.getElementById("precio3").onclick = function() {

            this.style.color = "green";
            this.style.fontWeight = "bold";

            alert("Producto seleccionado: " +
                document.getElementById("producto3").textContent +
                " - Precio: " +
                this.textContent);

        };


        document.getElementById("precio4").onclick = function() {

            this.style.color = "green";
            this.style.fontWeight = "bold";

            alert("Producto seleccionado: " +
                document.getElementById("producto4").textContent +
                " - Precio: " +
                this.textContent);

        };

    </script>

</body>

</html>
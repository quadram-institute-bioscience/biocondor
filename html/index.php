<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <meta name="description" content="">
  <meta name="author" content="">

  <title>Bare - Start Bootstrap Template</title>
  <!-- Bootstrap core CSS -->
  <link href="vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">

</head>

<body>
<?php
 include('inc/nav.php');
?>

  <!-- Page Content -->
  <div class="container">
    <div class="row">
      <div class="col-lg-12 text-center">
    <br>
<!-- TITLE -->
	    <h1>Package name<sup>version</sup></h1>
	    <div>
	        <a href="#" class="btn btn-default">Default</a>
	        <a href="#" class="btn btn-primary">Primary</a>
	        <a href="#" class="btn btn-success">Success</a>
	        <a href="#" class="btn btn-info">Info</a>
	        <a href="#" class="btn btn-warning">Warning</a>
	        <a href="#" class="btn btn-danger">Danger</a>
	    </div>
<!-- /TITLE -->

        <h1 class="mt-5">A Bootstrap 4 Starter Template</h1>
        <p class="lead">Complete with pre-defined file paths and responsive navigation!</p>
        <ul class="list-unstyled">
          <li>Bootstrap 4.3.1</li>
          <li>jQuery 3.4.1</li>
        </ul>

<?php include('inc/table.php'); ?>
      </div> <!-- col-l g-->
    </div> <!-- row -->
  </div> <!-- container -->



  <!-- Bootstrap core JavaScript -->
  <script src="vendor/jquery/jquery.slim.min.js"></script>
  <script src="vendor/bootstrap/js/bootstrap.bundle.min.js"></script>

</body>

</html>

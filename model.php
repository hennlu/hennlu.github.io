<?php require('mise_en_page_debut.php'); ?>
<div id='photo'>
<!-- mettre votre photo ici -->
<img src='medium_yoda.jpg' alt='Photo' height='120px' width='177px'>
</div>
<!-- ne pas modifier cette partie -->
<div id='cartouche_plus_bas'>
		<h1>Titre cartouche</h1>
		<div style="margin-bottom:10px;">
			Le D&eacute;partement de Math&eacute;matiques de la 
			<br><a href="http://old-www.u-psud.fr/Orsay">Facult&eacute; des Sciences d'Orsay</a>.
			<br/><br/>Contenu du cartouche.<br/><br/>	
			<hr/>
			<font color='#228050'>
					D&eacute;partement de Math&eacute;matiques<br/>
					B&acirc;timent 425<br/>
					Facult&eacute; des Sciences d'Orsay<br/>
					Universit&eacute; Paris-Sud 11<br/>
					F-91405 Orsay Cedex<br/>
					<br/>
			</font>
		</div>

</div>
<!-- modifier ici la valeur du margin-top en fonction de la hauteur de la photo -->
<!-- par exemple,si la photo fait X px de hauteur mettre margin-top:-X px --!>

<div id='contenu_avec_cartouche' style='margin-top:-120px'>
<?php 
include('contenu.html');
?>
</div>

<?php require('mise_en_page_fin.php'); ?>

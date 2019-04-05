<?php
// get contents of file in the form of an array
$files = file_get_contents($_FILES['file']['tmp_name']);
// splitting into an array of files
$files = preg_split('/\n/', $files);

// count number of file names
$numFiles = count($files);

// opening a process for each file
$processes = [];
for ($i = 0; $i < $numFiles; $i++)
	$processes[$i] = popen('python process.py "' . $files[$i] . '"', 'r');
?>

<!DOCTYPE html>
<html>
<head></head>
<body>

<style type="text/css">
	#window {
		margin: 0;
		width: 80%;
		height: 90%;
		z-index: 1000;
		display: none;
		padding: 5% 10%;
		background: white;
		position: absolute;
	}
	button:not(#close) {
		border: none;
		margin: .5% 0;
		min-width: 25%;
		padding-top: 1.5%;
		padding-bottom: 1.5%;
	}
</style>

<div id="window">
	<button id="close" onclick="document.getElementById('window').style.display = 'none';">X</button>
	<div id="info"></div>
</div>

<script type="text/javascript">
	function showInfo(info) {
		document.getElementById('info').innerHTML = info;
		document.getElementById('window').style.display = 'block';
	}
</script>

<?php
// iterating through each handler
$index = 0;
while ($index < $numFiles) {
	// getting output of each process till its not empty
	$content = '';
	do $content = stream_get_contents($processes[$index]);
	while (empty($content));
	// closing the process
	pclose($processes[$index++]);
	// echoing output in the form of HTML
	echo '<button onclick="showInfo(\'' . preg_replace('/\n/', '<br>', $content) . '\')">' . $files[$index-1] . '</button><br>';
}
?>

</body>
</html>
<?php
/**
 * Root PHP file
 *
 * Directs either to upload page, or processing page
 */
if ($_SERVER['REQUEST_METHOD'] === 'POST')
	require_once 'process.php';
else require_once 'upload.php';
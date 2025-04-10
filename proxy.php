<?php
// تحديد عنوان الـ API الذي ترغب في إرسال الطلبات إليه
$apiUrl = "http://207.180.223.38:5008/like";

// الحصول على المعلمات من الطلب
$uid = isset($_GET['uid']) ? $_GET['uid'] : '';
$key = isset($_GET['key']) ? $_GET['key'] : '';
$count = isset($_GET['count']) ? $_GET['count'] : '';

// التحقق من أن المعلمات موجودة
if (!$uid || !$key || !$count) {
    echo json_encode(['error' => 'Missing parameters']);
    exit;
}

// بناء رابط الطلب
$url = $apiUrl . "?uid=" . urlencode($uid) . "&key=" . urlencode($key) . "&count=" . urlencode($count);

// إرسال الطلب إلى الـ API
$response = file_get_contents($url);

// إرجاع النتيجة للموقع
header('Content-Type: application/json');
echo $response;
?>

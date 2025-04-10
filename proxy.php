<?php
// إضافة رأس CORS للسماح بالوصول من أي نطاق
header('Access-Control-Allow-Origin: *');
header('Content-Type: application/json');

// الحصول على المعلمات من الطلب
$uid = isset($_GET['uid']) ? $_GET['uid'] : '';
$key = isset($_GET['key']) ? $_GET['key'] : '';
$count = isset($_GET['count']) ? $_GET['count'] : '';

// التحقق من وجود المعلمات
if (!$uid || !$key || !$count) {
    echo json_encode(['error' => 'Missing parameters']);
    exit;
}

// تحديد رابط الـ API
$apiUrl = "http://207.180.223.38:5008/like?uid=" . urlencode($uid) . "&key=" . urlencode($key) . "&count=" . urlencode($count);

// استخدام cURL للحصول على البيانات من الـ API
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $apiUrl);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_TIMEOUT, 10); // تحديد مهلة الاتصال
$response = curl_exec($ch);

// إذا كان هناك خطأ في الاتصال بالخادم، سيتم إرجاع رسالة خطأ
if (curl_errno($ch)) {
    echo json_encode(['error' => 'API request failed: ' . curl_error($ch)]);
    exit;
}

curl_close($ch);

// فحص إذا كانت الاستجابة ليست JSON صحيحة
if ($response[0] == '<') {
    echo json_encode(['error' => 'Unexpected HTML response from the API. Response: ' . $response]);
    exit;
}

// إرجاع الاستجابة بتنسيق JSON
echo $response;
?>

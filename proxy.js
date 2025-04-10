const axios = require('axios');

module.exports = async (req, res) => {
  const { uid } = req.query;  // استلام UID من الرابط

  if (!uid) {
    return res.status(400).json({ error: 'UID is required' });
  }

  const apiUrl = `http://207.180.223.38:5008/like?uid=${uid}&key=brad&count=100`;

  try {
    // إرسال الطلب إلى API عبر HTTP
    const response = await axios.get(apiUrl);

    // التحقق مما إذا كانت الاستجابة بتنسيق JSON
    if (response && response.data) {
      res.json(response.data);  // إرسال البيانات إلى العميل
    } else {
      res.status(500).json({ error: 'Received empty or invalid response from API' });
    }

  } catch (error) {
    res.status(500).json({ error: 'Error occurred while sending likes', details: error.message });
  }
};

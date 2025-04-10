// api/proxy.js

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
    res.json(response.data);  // إرسال البيانات من API إلى العميل
  } catch (error) {
    res.status(500).json({ error: 'Error occurred while sending likes' });
  }
};

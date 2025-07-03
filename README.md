# 🛢️ China Oil Price for Home Assistant

Get current oil prices in China by region, integrated into Home Assistant.
更新版本：适配2025.6后的版本，

## 📦 Installation

### Via HACS (recommended)

1. Go to HACS → Integrations → Custom repositories
2. Add: `https://github.com/zhoujunn/oil-price-hacs`
3. Select category: `Integration`
4. Search & install “China Oil Price”
5. Restart Home Assistant

## ⚙️ Setup

Go to Home Assistant → Settings → Devices & Services → Add Integration → China Oil Price

### Required fields:
- **Name**: Display name (e.g. 南京油价)
- **Region**: Slug (e.g. `jiangsu`, `beijing`, `shanghai`, etc.)

## 💡 Example sensors

- 南京油价 92#：`7.58元/升`
- 南京油价 info：下次油价调整时间：2025年5月29日

---

📘 Data Source: [qiyoujiage.com](http://www.qiyoujiage.com)

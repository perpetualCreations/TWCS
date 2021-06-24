# TWCS
[![forthebadge](https://forthebadge.com/images/badges/contains-technical-debt.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

Flask web application for temporarily hosting redirected clients before a service restart/outage, before returning them to their referrer service after it is back online.
Replaces the need for web applications to implement their own handling of clients before server restarts and forseen outages.

## 3rd-Party Assets
For web sockets support, TWCS uses the SocketIO Javascript library,
loaded from [cdnjs.cloudflare.com](https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js). The authors of this project are not affiliated with the creators of SocketIO or its CDN distributor, you are encouraged to review [Cloudflare's Privacy Policy](https://www.cloudflare.com/privacypolicy/).

The stylesheet for the default redirect template is loaded from [dreamerslegacy.xyz](https://dreamerslegacy.xyz/css/schema.min.css), and is under the ownership of the project author(s).
Please review [privacy policies here](https://dreamerslegacy.xyz/html/privacy.html).

For users going off-grid, please review documentation regarding custom templates, and recommendations for using local assets.

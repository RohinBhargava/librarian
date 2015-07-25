<%inherit file="_dashboard_section.tpl"/>

<p>Change the wireless access point identifier (SSID).</p>

<form action="${i18n_url('plugins:ssid:changed')}" method="GET" class="inline">
  <input type="text" placeholder="SSID" name="name">
  <input type="hidden" value="no" name="reset">
  <button>${_('Save')}</button>
</form>

<form <form action="${i18n_url('plugins:ssid:changed')}" method="GET" class="inline">
  <button>${_('Reset')}</button>
  <input type="hidden" value="yes" name="reset">
</form>

<p>Note: You will need to reconnect to your device after you change the SSID.</p>

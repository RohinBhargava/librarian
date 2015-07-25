<%inherit file="../base.tpl"/>

<%block name="title">
## Translators, used as page title
${_('SSID Changed')}
</%block>

<%block name="heading">
## Translators, used as page heading
${_('Identifier reset')}
</%block>

% if name:
    <p>${_('The device name has successfully been changed to ')}<strong>${name}${_('!')}</strong></p>
% elif error:
    <p>${_('Changing the device name could not be completed. The following error occurred:')}</p>
    <p>${error}</p>
% endif

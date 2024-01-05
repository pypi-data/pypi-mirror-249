import traceback
import sys
from simo.multimedia.controllers import BaseAudioPlayer
from .gateways import SONOSGatewayHandler
from .forms import SONOSPlayerConfigForm


class SONOSPlayer(BaseAudioPlayer):
    gateway_class = SONOSGatewayHandler
    config_form = SONOSPlayerConfigForm

    def unjoin(self):
        from simo_sonos.models import SonosPlayer
        sonos_player = SonosPlayer.objects.filter(
            id=self.component.config['sonos_device']
        ).first()
        if not sonos_player:
            return
        try:
            sonos_player.soco.unjoin()
        except:
            print(traceback.format_exc(), file=sys.stderr)

    def play_uri(self, uri, volume=None):
        if volume:
            assert 0 <= volume <= 100
        self.send({"play_uri": uri, 'volume': volume})

    def play_alert(self, val, volume=None):
        '''Val can be sound id or uri'''
        assert type(val) in (int, str)
        if volume:
            assert 0 <= volume <= 100
        self.send({"alert": val, 'volume': volume})

    def play_playlist(self, item_id):
        from simo_sonos.models import SonosPlayer
        sonos_player = SonosPlayer.objects.filter(
            id=self.component.config['sonos_device']
        ).first()
        if not sonos_player:
            return
        for plst in sonos_player.soco.get_sonos_playlists():
            if plst.item_id == item_id:
                try:
                    sonos_player.soco.clear_queue()
                    sonos_player.soco.add_to_queue(plst)
                    sonos_player.soco.play_from_queue(0, False)
                    sonos_player.soco.play()
                    self.component.value = 'playing'
                    self.component.save()
                except:
                    print(traceback.format_exc(), file=sys.stderr)
                return

import time
import threading
from datetime import timedelta
from django.utils import timezone
from soco import discover, SoCo
from soco.snapshot import Snapshot
from simo.core.gateways import BaseObjectCommandsGatewayHandler
from simo.core.forms import BaseGatewayForm
from simo.core.models import Component
from simo.core.utils.helpers import get_self_ip
from simo.multimedia.models import Sound
from .models import SonosPlayer, SonosPlaylist
from .models import SonosPlayer
from .utils import get_sec


class SONOSGatewayHandler(BaseObjectCommandsGatewayHandler):
    name = "SONOS"
    config_form = BaseGatewayForm

    periodic_tasks = (
        ('periodic_players_discovery', 60 * 10),
        ('watch_players', 1)
    )

    playing_alerts = {}

    def perform_value_send(self, component, value):
        sonos_player = SonosPlayer.objects.get(id=component.config['sonos_device'])
        if value in (
            'play', 'pause', 'stop', 'next', 'previous',
        ):
            getattr(sonos_player.soco, value)()
        elif isinstance(value, dict):
            if 'seek' in value:
                sonos_player.soco.seek(timedelta(seconds=value['seek']))
            elif 'set_volume' in value:
                sonos_player.soco.volume = value['set_volume']
            elif 'shuffle' in value:
                sonos_player.soco.shuffle = value['shuffle']
            elif 'loop' in value:
                sonos_player.soco.repeat = value['loop']
            elif 'play_from_library' in value:
                if value['play_from_library'].get('type') != 'sonos_playlist':
                    return
                playlist = SonosPlaylist.objects.filter(
                    id=value['play_from_library'].get('id', 0)
                ).first()
                if not playlist:
                    return
                sonos_player.play_playlist(playlist)
            elif 'play_uri' in value:
                if value.get('volume') != None:
                    sonos_player.soco.volume = value['volume']
                sonos_player.soco.play_uri(value['play_uri'])
            elif 'alert' in value:
                try:
                    sound_id = int(value['alert'])
                except:
                    uri = value['alert']
                    length = None
                else:
                    sound = Sound.objects.get(pk=sound_id)
                    length = sound.length
                    uri = f"http://{get_self_ip()}{sound.get_absolute_url()}"

                threading.Thread(
                    target=self.play_alert, args=(
                        sonos_player, uri, length, value.get('volume')
                    )
                ).start()

        self.comp_state_update(component)


    def play_alert(self, sonos_player, uri, length, volume):
        if sonos_player.id not in self.playing_alerts:
            self.playing_alerts[sonos_player.id] = {
                'snap': Snapshot(sonos_player.soco),
                'uri': uri, 'timestamp': time.time()
            }
            self.playing_alerts[sonos_player.id]['snap'].snapshot()
        else:
            self.playing_alerts[sonos_player.id].update({
                'uri': uri, 'timestamp': time.time()
            })

        start_timestamp = self.playing_alerts[sonos_player.id]['timestamp']

        if volume != None:
            sonos_player.soco.volume = volume

        print("Play alert from URI: ", uri)
        sonos_player.soco.play_uri(uri)
        if length != None:
            if length > 60:
                length = 60
            time.sleep(length)
        else:
            for i in range(60):
                time.sleep(1)
                status = sonos_player.soco.get_current_transport_info()
                if status.get(
                    'current_transport_state', 'PLAYING'
                ) != 'PLAYING':
                    break

        if self.playing_alerts[sonos_player.id]['timestamp'] == start_timestamp \
        and self.playing_alerts[sonos_player.id]['uri'] == uri:

            print("Restore original")
            snap = self.playing_alerts[sonos_player.id]['snap']
            try:
                if snap.is_coordinator:
                    snap._restore_coordinator()
            finally:
                snap.device.mute = snap.mute
                snap.device.bass = snap.bass
                snap.device.treble = snap.treble
                snap.device.loudness = snap.loudness
                snap.device.volume = 0
                snap.device.ramp_to_volume(
                    snap.volume, ramp_type='AUTOPLAY_RAMP_TYPE'
                )

            # Now everything is set, see if we need to be playing, stopped
            # or paused ( only for coordinators)
            if snap.is_coordinator:
                if snap.transport_state == "PLAYING":
                    snap.device.play()
                elif snap.transport_state == "STOPPED":
                    snap.device.stop()

            del self.playing_alerts[sonos_player.id]

    def periodic_players_discovery(self):
        # Perform sonos players discovery and state check
        # of non playing players every 10 minutes
        self.discover_sonos_players()
        for comp in Component.objects.filter(
            gateway=self.gateway_instance, base_type='audio-player',
        ).exclude(value='playing'):
            self.comp_state_update(comp)

    def watch_players(self):
        for comp in Component.objects.filter(
            gateway=self.gateway_instance, base_type='audio-player',
            value='playing'
        ):
            self.comp_state_update(comp)
        time.sleep(1)

    def discover_sonos_players(self):
        print("Discover SONOS players.")

        discovered_players = []
        sonos_devices = list(discover(allow_network_scan=True))
        for sonos in sonos_devices:
            if sonos.group.coordinator.uid != sonos.uid:
                # Skip slave speakers save group masters only.
                continue
            player, new = SonosPlayer.objects.update_or_create(
                uid=sonos.uid, defaults={
                    'name': sonos.player_name, 'ip': sonos.ip_address,
                    'last_seen': timezone.now(), 'is_alive': True
                }
            )
            discovered_players.append(player)
            if new:
                print(f"New player - {player} - was found!")
            else:
                print(f"{player} - rediscovered.")

        missing_players = SonosPlayer.objects.exclude(
            id__in=[p.id for p in discovered_players]
        )
        if missing_players:
            print("Let's manually check the missing ones!")
            for missing_player in missing_players:
                try:
                    sonos = SoCo(missing_player.ip)
                    sonos.get_speaker_info()
                except:
                    print(
                        f"{missing_player} - still not available at {missing_player.ip}")
                    missing_player.is_alive = False
                    missing_player.save()
                else:
                    sonos_devices.append(sonos)
                    player, new = SonosPlayer.objects.update_or_create(
                        uid=sonos.uid, defaults={
                            'name': sonos.player_name, 'ip': sonos.ip_address,
                            'last_seen': timezone.now(), 'is_alive': True
                        }
                    )
                    if new:
                        print(f"New player - {player} - was found!")
                    else:
                        print(f"{player} - rediscovered.")

        print(
            "Figure out who's da boss "
            "and SONOS playlists that are available."
        )
        for sonos in sonos_devices:
            player = SonosPlayer.objects.get(uid=sonos.uid)
            if sonos.group.coordinator.uid == sonos.uid:
                player.slave_of = None
            else:
                player.slave_of = SonosPlayer.objects.filter(
                    uid=sonos.group.coordinator.uid
                ).first()
            player.save()

            playlists = []

            for pls in sonos.get_sonos_playlists():
                playlist, new = SonosPlaylist.objects.update_or_create(
                    item_id=pls.item_id,
                    player=SonosPlayer.objects.get(uid=sonos.uid),
                    defaults={'title': pls.title}
                )
                playlists.append(playlist)

            if playlists:
                for comp in Component.objects.filter(
                    gateway=self.gateway_instance, base_type='audio-player'
                ):
                    comp.meta['library'] = [
                        {'type': 'sonos_playlist',
                         'id': pls.id, 'title': pls.title}
                        for pls in playlists
                    ]
                    comp.save()

    def comp_state_update(self, sonos_component):
        print(f"Check {sonos_component} state!")
        sonos_player = SonosPlayer.objects.get(
            id=sonos_component.config['sonos_device']
        )
        try:
            status = sonos_player.soco.get_current_transport_info()
        except:
            sonos_component.value = 'stopped'
            sonos_component.alive = False
            sonos_component.save()
            return

        state_map = {
            'PLAYING': 'playing',
            'PAUSED_PLAYBACK': 'paused',
            'STOPPED': 'stopped'
        }
        sonos_component.value = state_map.get(
            status.get('current_transport_state', 'STOPPED'),
            'STOPPED'
        )

        try:
            info = sonos_player.get_current_track_info()
        except:
            sonos_component.alive = False
            sonos_component.save()
            return

        sonos_component.meta.update({
            'title': info['title'],
            'duration': get_sec(info['duration']),
            'position': get_sec(info['position']),
            'volume': sonos_player.soco.volume,
            'shuffle': sonos_player.soco.shuffle,
            'loop': sonos_player.soco.repeat,
        })

        sonos_component.save()

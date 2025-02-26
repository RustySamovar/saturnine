from game_server.protocol.cmd_id import CmdID
from game_server import HandlerRouter,Connection
from lib.proto import EnterSceneReadyReq,EnterScenePeerNotify,SceneInitFinishReq,SceneInitFinishRsp,WorldDataNotify,PropValue,HostPlayerNotify,PlayerGameTimeNotify,SceneTimeNotify,SceneDataNotify,WorldPlayerInfoNotify,OnlinePlayerInfo,ScenePlayerInfoNotify,ScenePlayerInfo,PlayerEnterSceneInfoNotify,SceneInitFinishRsp,GetScenePointReq, GetSceneAreaReq,GetScenePointRsp,GetSceneAreaRsp
from lib.retcode import Retcode
import enet

router = HandlerRouter()

@router(CmdID.EnterSceneReadyReq)
def handle_scene_ready(conn: Connection, msg: EnterSceneReadyReq):
    enter_scene_peer_notify = EnterScenePeerNotify()
    enter_scene_peer_notify.peer_id = 1
    enter_scene_peer_notify.host_peer_id = 1
    enter_scene_peer_notify.dest_scene_id = conn.player.scene_id
    conn.send(enter_scene_peer_notify)

@router(CmdID.SceneInitFinishReq)
def handle_scene_init(conn: Connection, msg: SceneInitFinishReq):

    online_player_info = OnlinePlayerInfo(uid=conn.player.uid, nickname=conn.player.name)

    world_data_notify = WorldDataNotify()
    world_data_notify.world_prop_map = {
        1: PropValue(1, ival=8),
        2: PropValue(2, ival=0)
    }

    host_player_notify = HostPlayerNotify()
    host_player_notify.host_uid = conn.player.uid
    host_player_notify.host_peer_id = 1

    player_game_time_notify = PlayerGameTimeNotify()
    player_game_time_notify.game_time = 0
    player_game_time_notify.uid = conn.player.uid

    scene_time_notify = SceneTimeNotify()
    scene_time_notify.scene_id = conn.player.scene_id
    scene_time_notify.scene_time = 0
    scene_time_notify.is_paused = False

    scene_data_notify = SceneDataNotify()
    scene_data_notify.level_config_name_list = ["Level_BigWorld"]

    world_player_info_notify = WorldPlayerInfoNotify()
    world_player_info_notify.player_info_list = [online_player_info]
    world_player_info_notify.player_uid_list = [conn.player.uid]

    scene_player_info_notify = ScenePlayerInfoNotify()
    scene_player_info_notify.player_info_list = [ScenePlayerInfo(conn.player.uid, 1, conn.player.name, True, conn.player.scene_id, online_player_info)]

    enter_scene_info_notify = PlayerEnterSceneInfoNotify()
    enter_scene_info_notify.cur_avatar_entity_id = 1

    conn.send(world_data_notify)
    conn.send(host_player_notify)
    conn.send(player_game_time_notify)
    conn.send(scene_time_notify)
    conn.send(world_player_info_notify)
    conn.send(scene_player_info_notify)
    conn.send(enter_scene_info_notify)

@router(CmdID.GetScenePointReq)
def handle_scene_point(conn: Connection, msg: GetScenePointReq):
    rsp = GetScenePointRsp()
    rsp.scene_id = msg.scene_id
    rsp.unlocked_point_list = []
    rsp.unlock_area_list = []
    for x in range(200):
        rsp.unlock_area_list.append(x)
        rsp.unlocked_point_list.append(x)
    conn.send(rsp)

@router(CmdID.GetSceneAreaReq)
def handle_scene_area(conn: Connection, msg: GetSceneAreaReq):
    rsp = GetSceneAreaRsp()
    rsp.scene_id = msg.scene_id
    rsp.area_id_list = []
    for x in range(200):
        rsp.area_id_list.append(x)
    conn.send(rsp)

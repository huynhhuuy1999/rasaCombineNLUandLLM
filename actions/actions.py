import os
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from dotenv import load_dotenv

from actions.db import get_driver

load_dotenv()  


NEO4J_DATABASE = os.getenv("NEO4J_DATABASE")

class toChucNghiLeAction(Action):

    def name(self) -> str:
        return "toChucNghiLeAction"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[str, Any]):
        drv = get_driver()
        with drv.session() as session:
            # route = tracker.get_slot("route_session_to_calm")
            session = drv.session(database=NEO4J_DATABASE)
            result = session.run("MATCH (a:Answer)-[:BELONG_TO]->(i:Intent {name:\"ToChucNghiLe\"}) return a;").data()
            if result:
                answers = [record['a']['answer'] for record in result]
                dispatcher.utter_message(text=', '.join(answers))
            else:
                dispatcher.utter_message(text="Xin lỗi tôi không thể trả lời câu hỏi của bạn")
        # drv.close()
        return []
class trachNhiemVaQuyenHanAction(Action):

    def name(self) -> str:
        return "trachNhiemVaQuyenHanAction"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[str, Any]):
        drv = get_driver()
        with drv.session() as session:
            session = drv.session(database=NEO4J_DATABASE)
            position = tracker.get_slot("position")
            print('position', position)
            # route = tracker.get_slot("route_session_to_calm")
            answers = None
            entity = ""
            entities = tracker.latest_message['entities']
            print('entities', entities)
            
            if position == "giảng viên":
                entity = "GiangVien"
            elif position == "cán bộ chiến sĩ":
                entity = "CBCS"
            elif position == "giảng viên thỉnh giảng":
                entity = "GiangVienThinhGiang"
            if entity:
                result = session.run(f"MATCH (a:Answer {{entity:\"{entity}\"}})-[:BELONG_TO]->(i:Intent {{name:\"TrachNhiemVaQuyenHan\"}}) return a.answer LIMIT 1;").data()
                
                if result:
                    answers = [record['a.answer'] for record in result]
            if answers:
                dispatcher.utter_message(text=', '.join(answers))
            else:
                dispatcher.utter_message(text="Xin lỗi tôi không thể trả lời câu hỏi của bạn")
            
        return []
class quyTrinhXayDungChuongTrinhCongTacAction(Action):
    
    def name(self) -> str:
        return "quyTrinhXayDungChuongTrinhCongTacAction"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[str, Any]):
        drv = get_driver()
        with drv.session() as session:
            session = drv.session(database=NEO4J_DATABASE)
            
            
            intent = tracker.latest_message.get('intent', {}).get('name')
            # a = tracker.latest_message.get('entities', [])
            entities = tracker.latest_message['entities']
            
            dispatcher.utter_message(text="Xin lỗi tôi không thể trả lời câu hỏi của bạn")
        
        return []
import json
import unittest

from paik2json.line_manager import LineManager
from paik2json.parser import Parser


raw_메모_예시1 = """day-2023-12-27-D0
  일일보고-D1
    한일-D2
      문서 쓰기
      코드 짜기
    할일-D2
      문서 읽기
      코드 실행하기
  토픽1-D1
    할일1-D2
      뭔가 해야함
      할 게 많음
    할일2-D2
    할일3-D2
  토픽2-D1
    할 게 별로 없음-D2
    할일4-D2
"""

raw_메모_예시2 = """2023-12-28(목)
  did
    🕹️ [ABC-1] 책장 정리하기
    🕹️ [ABC-12] 검색 폼 생성
  willdo
    🕹️ [ABC-123] 검색 기능 추가
    🕹️ [ABC-1234] 책 등록하기

  🕹️ [ABC-123] 검색 기능 추가
    하나씩 처리
    두개씩 처리
    세개씩 처리

2023-12-27(수)
  did
    🕹️ [ABC-9] 책장 구상하기
    🕹️ 휴가
  willdo
    🕹️ [ABC-1] 책장 정리하기
    🕹️ [ABC-12] 검색 폼 생성

  🕹️ [ABC-12] 검색 폼 생성
    검색 폼 UI 제작
    반응형 적용
"""


class ParserTestCase(unittest.TestCase):
    def setUp(self):
        self.parser1 = Parser(raw_메모_예시1)
        self.parser2 = Parser(raw_메모_예시2)
        self.parser3 = Parser(raw_메모_예시2)
        self.maxDiff = None

    def test_parse_hook_으로_문자열을_변경할_수_있다(self):
        expected1 = json.loads(
            """{"2023-12-28(목)⭐️": {"did⭐️": ["🕹️ [ABC-1] 책장 정리하기⭐️","🕹️ [ABC-12] 검색 폼 생성⭐️"],"willdo⭐️": ["🕹️ [ABC-123] 검색 기능 추가⭐️","🕹️ [ABC-1234] 책 등록하기⭐️"],"🕹️ [ABC-123] 검색 기능 추가⭐️": ["하나씩 처리⭐️","두개씩 처리⭐️","세개씩 처리⭐️"]},"2023-12-27(수)⭐️": {"did⭐️": ["🕹️ [ABC-9] 책장 구상하기⭐️","🕹️ 휴가⭐️"],"willdo⭐️": ["🕹️ [ABC-1] 책장 정리하기⭐️","🕹️ [ABC-12] 검색 폼 생성⭐️"],"🕹️ [ABC-12] 검색 폼 생성⭐️": ["검색 폼 UI 제작⭐️","반응형 적용⭐️"]}}"""
        )
        result1 = Parser(raw_메모_예시2, hook=(lambda x: x + "⭐️")).parse()
        self.assertDictEqual(expected1, result1)

        expected2 = json.loads(
            """{"2023-12-28(목)": {"did": ["🕹️ [DEF-1] 책장 정리하기","🕹️ [DEF-12] 검색 폼 생성"],"willdo": ["🕹️ [DEF-123] 검색 기능 추가","🕹️ [DEF-1234] 책 등록하기"],"🕹️ [DEF-123] 검색 기능 추가": ["하나씩 처리","두개씩 처리","세개씩 처리"]},"2023-12-27(수)": {"did": ["🕹️ [DEF-9] 책장 구상하기","🕹️ 휴가"],"willdo": ["🕹️ [DEF-1] 책장 정리하기","🕹️ [DEF-12] 검색 폼 생성"],"🕹️ [DEF-12] 검색 폼 생성": ["검색 폼 UI 제작","반응형 적용"]}}"""
        )
        result2 = Parser(raw_메모_예시2, hook=(lambda x: x.replace("ABC", "DEF"))).parse()
        self.assertDictEqual(expected2, result2)

    def test_parser_가_인자로_문자열을_받을_수있다(self):
        expected = json.loads(
            """{"2023-12-28(목)": {"did": ["🕹️ [ABC-1] 책장 정리하기","🕹️ [ABC-12] 검색 폼 생성"],"willdo": ["🕹️ [ABC-123] 검색 기능 추가","🕹️ [ABC-1234] 책 등록하기"],"🕹️ [ABC-123] 검색 기능 추가": ["하나씩 처리","두개씩 처리","세개씩 처리"]},"2023-12-27(수)": {"did": ["🕹️ [ABC-9] 책장 구상하기","🕹️ 휴가"],"willdo": ["🕹️ [ABC-1] 책장 정리하기","🕹️ [ABC-12] 검색 폼 생성"],"🕹️ [ABC-12] 검색 폼 생성": ["검색 폼 UI 제작","반응형 적용"]}}"""
        )
        result = Parser(raw_메모_예시2).parse()
        self.assertDictEqual(expected, result)

    def test_parse_로_JSON_변경시_마지막_노드는_빈_배열이_된다(self):
        expected1 = {
            "day-2023-12-27-D0": {
                "일일보고-D1": {
                    "한일-D2": ["문서 쓰기", "코드 짜기"],
                    "할일-D2": ["문서 읽기", "코드 실행하기"],
                },
                "토픽1-D1": {
                    "할일1-D2": ["뭔가 해야함", "할 게 많음"],
                    "할일2-D2": [],
                    "할일3-D2": [],
                },
                "토픽2-D1": ["할 게 별로 없음-D2", "할일4-D2"],
            }
        }
        result1 = self.parser1.parse()
        self.assertDictEqual(expected1, result1)

    def test_parse_로_JSON_변경시_마지막_노드가_모두_비었을_경우_부모_노드는_문자열의_배열을_갖는다(self):
        expected1 = {
            "day-2023-12-27-D0": {
                "일일보고-D1": {
                    "한일-D2": ["문서 쓰기", "코드 짜기"],
                    "할일-D2": ["문서 읽기", "코드 실행하기"],
                },
                "토픽1-D1": {
                    "할일1-D2": ["뭔가 해야함", "할 게 많음"],
                    "할일2-D2": [],
                    "할일3-D2": [],
                },
                "토픽2-D1": ["할 게 별로 없음-D2", "할일4-D2"],
            }
        }
        result1 = self.parser1.parse()

        self.assertDictEqual(expected1, result1)

    def test_parse_로_테이블을_JSON_으로_변경할_수_있다(self):
        expected1 = {
            "day-2023-12-27-D0": {
                "일일보고-D1": {
                    "한일-D2": ["문서 쓰기", "코드 짜기"],
                    "할일-D2": ["문서 읽기", "코드 실행하기"],
                },
                "토픽1-D1": {
                    "할일1-D2": ["뭔가 해야함", "할 게 많음"],
                    "할일2-D2": [],
                    "할일3-D2": [],
                },
                "토픽2-D1": ["할 게 별로 없음-D2", "할일4-D2"],
            }
        }
        result1 = self.parser1.parse()
        self.assertDictEqual(expected1, result1)

        expected2 = json.loads(
            """{"2023-12-28(목)": {"did": ["🕹️ [ABC-1] 책장 정리하기","🕹️ [ABC-12] 검색 폼 생성"],"willdo": ["🕹️ [ABC-123] 검색 기능 추가","🕹️ [ABC-1234] 책 등록하기"],"🕹️ [ABC-123] 검색 기능 추가": ["하나씩 처리","두개씩 처리","세개씩 처리"]},"2023-12-27(수)": {"did": ["🕹️ [ABC-9] 책장 구상하기","🕹️ 휴가"],"willdo": ["🕹️ [ABC-1] 책장 정리하기","🕹️ [ABC-12] 검색 폼 생성"],"🕹️ [ABC-12] 검색 폼 생성": ["검색 폼 UI 제작","반응형 적용"]}}"""
        )
        result2 = self.parser2.parse()
        self.assertDictEqual(expected2, result2)

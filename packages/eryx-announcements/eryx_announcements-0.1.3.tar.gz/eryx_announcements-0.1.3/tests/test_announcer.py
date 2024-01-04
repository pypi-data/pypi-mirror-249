from tests.mocks import AnnouncementMockB, Announced, AnnouncementMockA


class TestAnnouncer:
    def test_when_a_subscribed_announcement_happens_then_the_configured_action_is_sent(self, announcer):
        announced = Announced()
        announcer.subscribe(AnnouncementMockA, announced.do_something)
        an_announcement = announcer.announce(AnnouncementMockA())
        self._assert_only_was_sent(an_announcement, announced)

    def test_when_a_not_subscribed_announcement_happens_then_the_configured_action_is_not_sent(self, announcer):
        announced = Announced()
        announcer.subscribe(AnnouncementMockB, announced.do_something)
        announcer.announce(AnnouncementMockA())
        self._assert_none_was_sent(announced)

    def test_when_an_unsubscribed_announcement_happens_then_the_configured_action_is_not_sent(self, announcer):
        announced = Announced()
        announcer.subscribe(AnnouncementMockA, announced.do_something)
        announcer.unsubscribe(announced.do_something)
        announcer.announce(AnnouncementMockA())
        self._assert_none_was_sent(announced)

    def _assert_only_was_sent(self, an_announcement, announced):
        assert len(announced.announcements()) == 1
        assert announced.announcements()[0] == an_announcement

    def _assert_none_was_sent(self, announced):
        assert len(announced.announcements()) == 0

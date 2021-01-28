from lib.action import St2BaseAction

__all__ = [
    'St2InquiryRespondAction'
]


class St2InquiryRespondAction(St2BaseAction):

    def run(self, id, response):
        self.client.inquiries.respond(inquiry_id=id,
                                      inquiry_response=response)

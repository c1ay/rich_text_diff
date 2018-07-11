# -*- coding: utf-8 -*-
import unittest
import rich_text_diff

new_content = u'<p>\u4eca\u5929\u5929\u6c14\u8fd8\u4e0d\u9519</p><p>\u4eca\u5929\u5929\u6c14\u8fd8\u4e0d\u9519</p><img src="v2-0fdfbce4409625a81e0bd210baf4a7ee.jpg" data-caption="" data-size="normal" data-rawwidth="640" data-rawheight="618" data-watermark="watermark" data-original-src="v2-0fdfbce4409625a81e0bd210baf4a7ee" data-watermark-src="v2-c53c9358c4191a0348eaf3324d20cbfa" data-private-watermark-src=""><p>\u4eca\u5929\u5929\u6c14\u8fd8\u4e0d\u9519</p><video id="None" data-swfurl="" poster="https://pic2.zhimg.com/80/v2-d98a74d35a1d369fd07b1aba5a5e2071_b.jpg" data-sourceurl="https://www.zhihu.com/video/987659040658411520" data-name="" data-video-id="" data-video-playable="true" data-lens-id="987659040658411520"></video><p></p>'
old_content = u'<p>\u4eca\u5929\u5929\u6c14\u8fd8233</p><p>\u4eca\u5929\u5929\u6c14\u8fd8\u4e0d\u9519</p><img src="v2-0fdfbce4409625a81e0bd210baf4a7ee.jpg" data-caption="\u56fe\u7247\u6ce8\u91ca233" data-size="normal" data-rawwidth="640" data-rawheight="618" data-watermark="watermark" data-original-src="v2-0fdfbce4409625a81e0bd210baf4a7ee" data-watermark-src="v2-c53c9358c4191a0348eaf3324d20cbfa" data-private-watermark-src=""><p><br></p><img src="v2-724ec2687676e21539028c54a317a491.jpg" data-caption="" data-size="normal" data-rawwidth="363" data-rawheight="393" data-watermark="watermark" data-original-src="v2-724ec2687676e21539028c54a317a491" data-watermark-src="v2-5cfd32fae8f6254e904c12a95cd1a0b9" data-private-watermark-src=""><p>\u4eca\u5929\u5929\u6c14\u8fd8\u4e0d\u9519</p><video id="None" data-swfurl="" poster="https://pic2.zhimg.com/80/v2-d98a74d35a1d369fd07b1aba5a5e2071_b.jpg" data-sourceurl="https://www.zhihu.com/video/987659040658411520" data-name="\u89c6\u9891\u6807\u9898233" data-video-id="" data-video-playable="true" data-lens-id="987659040658411520"></video><video id="None" data-swfurl="" poster="https://pic1.zhimg.com/80/v2-9b44fdebaec8e7cf8b24d934a914c454_b.jpg" data-sourceurl="https://www.zhihu.com/video/987663649024090113" data-name="" data-video-id="" data-video-playable="true" data-lens-id="987663649024090113"></video><p></p>'


class TestDiff(unittest.TestCase):

    def test_diff(self):
        d = rich_text_diff.ContentDiff(new_content, old_content)
        d.diff()

    def test_ensure_closed_tag(self):
        ret = rich_text_diff.ensure_closed_tag(' ')
        self.assertEqual('<div></div>', ret)
        rich_text_diff.ensure_closed_tag('<p>')


if __name__ == '__main__':
    unittest.main()

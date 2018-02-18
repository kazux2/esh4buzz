# coding: UTF-8

import MeCab



class TextSegmentation(object):



    hiragana = []

    def __init__(self, args=(12353, 12436)):
        # アルファベット小文字→(97, 123)
        # アルファベット大文字→(65, 91)
        # 半角数字→(48, 58)
        # ひらがな→(12353, 12436)
        # カタカナ→(12449, 12532+1)
        # 全角数字→(65296, 65306)
        self.hiragana = [chr(i) for i in range(12353, 12436)]



    def segment_text(self, text, limit = 99):

        mecab = MeCab.Tagger("-Ochasen")
        mecab.parse('')
        node = mecab.parseToNode(text)


        r_dict = {}
        count = 0

        node = node.next #because of this bug : https://github.com/SamuraiT/mecab-python3/issues/3
        while len(r_dict)<limit:

            if isinstance(node,type(None)):
                break

            elif node.feature.split(",")[0] == "名詞" and node.surface not in self.hiragana:
                r_dict.setdefault(count, [])
                r_dict[count].append("{}".format(node.surface))

            elif node.feature.split(",")[0] == "動詞" and node.feature.split(",")[1] == "自立" and node.surface not in self.hiragana:
                try:
                    r_dict[count] = r_dict[count]
                except KeyError:
                    r_dict.setdefault(count, [])

                r_dict[count].append("{}".format(node.surface))

            elif (node.feature.split(",")[0] == "記号" and node.feature.split(",")[1] == "句点") \
                or (node.feature.split(",")[0] == "記号" and node.feature.split(",")[1] == "読点"):

                try:
                    r_dict[count] = r_dict[count]
                    count += 1
                except KeyError:
                    pass

            node = node.next

        return r_dict



    def join_dict_elements(self, r_dict, minimum_elements = 3):

        for i in range(len(r_dict)):
            if len(r_dict[i]) <minimum_elements:
                r_dict.pop(i)
            else:
                r_dict[i] = " ".join(r_dict[i])

        return r_dict



    def reindex_r_dict(self, r_dict):

        refined_r_dict = {}
        dict_index = 0

        for i in r_dict.keys():
            refined_r_dict[dict_index] = r_dict[i]
            dict_index += 1

        return refined_r_dict



# def just_mecabbing(keyword):
#     mecab = MeCab.Tagger("-Ochasen")
#     mecab.parse('')
#     node = mecab.parseToNode(keyword)
#
#     node = node.next
#     while node:
#         print(node.surface + "  " + node.feature)
#         node = node.next

#sample text
keyword1 = "完璧な文章などといったものは存在しない。完璧な絶望が存在しないようにね。"
keyword2 = "重ねて言いますが、勉強とはノーマライゼーション、つまり“よりノーマルへと近づき、ノーマルな基準の中で偉くなること”ではありません。ノーマルの基準からズレたところで、ノーマルな人たちに後ろ指さされながらも、そこで独自のフィールドを展開すること。これこそがこの本で提唱する“勉強”なんです。"
keyword3 = "いわゆる受験戦争を乗り越えてきた人たちはみな、勉強を頑張ったことで周囲とズレが生じたというトラウマがあるんです。『勉強の哲学』を書くにあたり、そういった人たちが共感できる部分をあえて集めたところはあります。なぜなら、このトラウマに焦点を当てた本というのが今までなかったからです。学校の勉強なんてクソくらえだ！”という感じで生きてきた人が自分なりのやり方を貫いて成功した話、勉強しなかった人への応援歌といったものはたくさん書かれているのに、逆に勉強したことで不幸になった人への応援歌はなかった。きっと多くの人は、勉強すると何かトクをするとか、社会的にいい立場に行けると思っているんでしょうね。でも必ずしもそうじゃない。勉強することで、みんなが楽しめることが自分だけ楽しめなくなる、ノーマルさを失うということがある。これは『勉強の哲学』の大切なテーマです。"
keyword4 = "無料で漫画や書籍を公開し、閲覧数に応じて広告収益などを得ているタダ読みサイトは、あとをたたない。著作権法違反事件として逮捕者も出ており、集英社や講談社、小学館など出版大手各社は「絶対に看過することはできない」としている。久世さんのツイートに、出版社からも共感する声が出ている。小学館「&フラワー」編集部の公式アカウントは「正直、明らかに売り上げに影響出ています。このままだと違法サイトのせいで、漫画が世の中から無くなります...。」と危機感を示した。ハフポスト日本版は、投稿を通じて伝えたかったことについて、久世さんにTwitterで取材した。——なぜ今、タダ読みサイトへの注意喚起を促すツイートをしたのですか。タイミングは今がベストかと言うとそうでもないのかもしれません。もっと早くても良かったかなと思います。この問題については以前から認識していましたが、個人でどうこうできる問題でもなく作家は著作権を侵害されながらも現状泣き寝入りするしかないともわかっておりました。ですが、ごく当たり前にネット上の簡単に目に付く位置に違法サイトのリンクが用意されていることで、違法サイトだと知らずに利用している方も日に日に増えているように感じていました。漫画の中でも書いていますが、悪いことは悪いのだと、また何故悪いのかということをわかりやすく伝えたかったというのが大きいです。微力ながら、ツイートをご覧頂くそれぞれの方のモラルの面に語りかけることで問題提起ができれば...という気持ちでした。"
keyword5 = "成人の日の1月8日早朝、多くの新成人が予約金を支払っていた振り袖販売やレンタルを手掛ける業者「はれのひ（harenohi）」が突如行方不明になったという被害報告がネット上で相次いでいる。  ハフポスト日本版の取材に対して、同社で振り袖を購入、着付け予定だった大学生の女性（20）は「一生に一度しかない晴れ舞台を、こんな形にされて、悲しい気持ちもたくさんあるし、2度とこんなことが起こってほしくない」と話している。  女性は、「はれのひ」横浜みなとみらい店で振り袖を購入。着付けの会場となった近隣のホテルに直接届けてもらう形とし、成人式に向かうため、1月8日早朝から同社に着付けを依頼していた。  段取りに手間取る場面があり、2日前に電話をした際には「振袖はこちらでホテルまで郵送するので、心配しなくて大丈夫です。成人おめでとうございます」と言われたという。  しかし、8日早朝、同じ会場で着付けをしてもらう予定だった友人から「ホテルに業者が来ておらず、振り袖も届いていない」との連絡を受けた。女性も慌てて会場に向かったが、スタッフと連絡を取ることができなかったという。  女性によると会場は「パニック状態」だが、着付け会場のホテルスタッフや会場として利用していた他のレンタル業者らが協力して、着付けや振り袖を探すなどのサポートをしていたという。「人の優しさが身にしみます」と話している。"
keyword6 = "子宮や卵巣に病気が見つかったと聞いたら、どう思うだろうか？ 将来妊娠できなくなるのでは？ 身体にメスが入るの？ それもモデルという、人に見られる仕事をしている彼女だ。「私、高校生の時に前十字靭帯を断絶していて、手術は3回しているので、全身麻酔は慣れっこ（笑）。もちろん少しは悲劇のヒロインモードにもなりましたけど、こういう星のもとに生まれたんだなぁって」入院は1週間程度。手術による妊娠への支障はないという。「この病気って、女の子の10人に1人がなるって言われているくらいよくあるものらしくて、そのぶん、治療技術も発達してるんですよね。どの病院に行ってもしっかり治せるって言われてたので」"



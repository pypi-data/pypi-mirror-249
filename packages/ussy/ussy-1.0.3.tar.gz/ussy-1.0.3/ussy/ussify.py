from eng_syl.syllabify import Syllabel
from eng_syl.phonify import onc_to_phon

class Ussy():
    def __init__(self, min_len=3):
        self.piss = Syllabel()
        self.shit = onc_to_phon()
        self.min_len = min_len
        self.explosive_list = ['m', 'p', 'r', 'b', 't', 'k', 'f', 'l','ɹ', 'dʒ','n','g']

        onsets = ['bl', 'br', 'cl', 'cr', 'dr', 'fl', 'fr', 'gl', 'gr', 'pl', 'pr', 'sk', 'sl', 'sm', 'sn',
                  'sp', 'st', 'str', 'sw', 'tr', 'ch', 'sh', 'm', 'c', 'b', 'r', 'd', 'h', 's', 'p', 'l', 'g', 'f', 'w',
                  't', 'k', 'n', 'v', 'st', 'pr', 'j', 'br', 'ch', 'gr', 'sh',
                  'tr', 'cr', 'fr', 'z', 'sp', 'wh', 'cl', 'y', 'bl', 'th', 'fl', 'sch', 'pl', 'q', 'dr', 'str', 'sc',
                  'sl', 'kr', 'sw', 'gl',
                  'ph', 'kl', 'sm', 'sn', 'kn', 'sk', 'mcc', 'scr', 'wr', 'mc', 'chr', 'spr', 'thr', 'tw', 'schw',
                  'mcg', 'mck', 'rh',
                  'sq', 'schl', 'shr', 'schr', 'x', 'schm', 'mcm', 'gh', 'mcn', 'hyp', 'mccl', 'schn', 'mcd', 'hydr',
                  'kh', 'ts',
                  'mcl', 'spl', 'dw', 'pf', 'mccr', 'mcf', 'typ', 'cz', 'sr', 'cycl', 'gn', 'hr', 'hy', 'syn', 'sz',
                  'kw', 'dyn', 'phys', 'symb', 'dyn', 'symb']

        nuclei = ['a', 'e', 'i', 'o', 'u', 'oo', 'ia', 'ie', 'ee', 'io', 'au', 'ea', 'ou', 'ai', 'ue', 'ei', 'eau',
                  'eu', 'oe', 'ae', 'eo',
                  'oa', 'oo', 'ao', 'ua', 'oi', 'ui', 'aa', 'ieu', 'uo', 'oia', 'aue', 'iu', 'aia', 'iou', 'ii', 'aio',
                  'uie', 'eia', 'iao', 'y', 'uh',
                  'ay', 'ey', 'ah', 'eh', 'oh', 'oy', 'aigh', 'igh', 'eigh', 'aw', 'ow', 'ew', 'ye', 'ooh', 'owe',
                  'awe', 'ore', 'er', 'or', 'ere',
                  'are', 'ar', 'ur', 'ir', 'ire', 'ue', 'eye', 'aye', 'ye', 'uy']

        codas = ['ct', 'ft', 'mp', 'nd', 'ng', 'nk', 'nt', 'pt', 'sk', 'sp', 'ss', 'st', 'ch', 'sh', 's', 'n', 'r', 'd',
                 'ng', 'l', 'rs', 'ns', 't', 'm', 'll', 'nt', 'c', 'ck', 'st', 'k', 'ss', 'sts', 'rd', 'nd',
                 'ry', 'rt', 'w', 'lly', 'tt', 'ch', 'ts', 'ty', 'p', 'ls', 'ld', 'nts', 'x', 'rg', 'sh', 'ly', 'th',
                 'ff', 'g', 'rn', 'ngs',
                 'nn', 'tz', 'sm', 'gh', 'ms', 'z', 'cs', 'ps', 'ds', 'b', 'lt', 'nk', 'nds', 'ys', 'rk', 'ght', 'v',
                 'cks', 'f', 'ct',
                 'rth', 'rry', 'lls', 'ny', 'ws', 'cts', 'wn', 'rds', 'dy', 'bly', 'rts', 'ft', 'hl', 'gy', 'pp', 'rly',
                 'mp', 'ntly',
                 'sch', 'ngly', 'sly', 'ks', 'tch', 'ncy', 'rm', 'gs', 'rty', 'hn', 'fy', 'rst', 'rr', 'ntz', 'bs',
                 'cy', 'dly', 'tts']

        self.onsets = sorted(sorted(set(onsets)), key=len, reverse=True)

        self.nuclei = sorted(sorted(set(nuclei)), key=len, reverse=True)

        self.codas = sorted(sorted(set(codas)), key=len, reverse=True)

    def onc_split(self, word):
        for i in self.onsets:
            if word.startswith(i):
                i_less = word.replace(i, '', 1)
                for n in self.nuclei:
                    if i_less.startswith(n):
                        n_less = i_less.replace(n, '')
                        return i + '-' + n + '-' + n_less
                break
        for n in self.nuclei:
            if word.startswith(n):
                i = ''
                n_less = word.replace(n, '')
                return n + '-' + n_less
            elif n in word:
                onset, coda = word.split(n, 1)
                return '-'.join([onset, n, coda])
        return "the rizzlord"

    def ussify(self, word, plural=False):
        oncs, phons = self.conv_ipa(word)
        if oncs and phons:
            ussied = self.ussy_check(oncs, phons, plural)
            if(ussied):
                return ussied
            else:
                return False
        else:
            return False

    def conv_ipa(self, word):
        prediction = self.piss.syllabify(word)
        nuclei_onsets = '-'.join([self.onc_split(x.lower()).strip('-') for x in prediction.split('-')]).split('-')
        if "the rizzlord" not in nuclei_onsets:
            phon_prediction = self.shit.ipafy(nuclei_onsets)
            return nuclei_onsets, phon_prediction
        else:
            return [],[]

    def ussy_check(self, oncs, phons, plural):

        i = len(phons) - 1

        if(i + 1 < self.min_len and (phons[i] in self.explosive_list)):
            if plural:
                return ''.join(oncs) + "ussies"
            else:
                return ''.join(oncs) + "ussy"

        while(i > 0):
            phons.pop(i)
            oncs.pop(i)
            i -= 1
            if any(phons[i].endswith(plosive) for plosive in self.explosive_list):
                if plural:
                    return ''.join(oncs) + "ussies"
                else:
                    return ''.join(oncs) + "ussy"
        return False

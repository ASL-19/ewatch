# -*- coding: utf-8 -*-
# Election Watch - To enable responsive governance and informed engagement with presidential elections
#
# Copyright (C) 2016  ASL19
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals
import logging
import sys
import os
import re
import threading
from django.db import transaction
from django.db.models import Q
# XXX: NLP Toolkit, note that the specifics of function calls
# are dependendent on the NLP toolkit you are using
from NLPToolkit import (           # noqa: E402
    Normalizer,
    WordTokenize,,
    Lemmatizer,
    StopWords,
    POSTagger,
)


LOGGER = logging.getLogger()


def should_stay(word):

    digits = r'.*[0123456789۰۱۲۳۴۵۶۷۸۹]+.*'

    if len(word) < 2:
        return False
    # XXX: StopWords part of NLP toolkit
    if word in StopWords.words():
        return False
    if re.search(r'.*[a-zA-Z]+.*', word) is not None:
        return False
    if re.search(digits, word) is not None:
        return False

    return True


def prepare_text(text):

    from models import StopWord, NamedEntity

    farsi_puncs = '!:\.،؛؟»\]\)\}«\[\(\{'
    lemmatized_words = []

    # XXX: Normalizer part of NLP toolkit
    normalizer = Normalizer()
    text = normalizer.normalize(text)
    LOGGER.info('NORM = ' + unicode(text))

    replace_pattern = re.compile(r'[\s' + farsi_puncs + ']+')
    text = re.sub(replace_pattern, ' ', text)

    named_entities = NamedEntity.objects.all()
    ne_words = []
    for ne in named_entities:
        count = len(re.findall(ne.name, text))
        LOGGER.info("{} for {} times".format(ne.name, str(count)))
        text = re.sub(ne.name, '', text)
        for c in range(count):
            ne_words.append((ne.name, ne.name))

    LOGGER.info('NE REMOVED TEXT = ' + text)
    LOGGER.info("NE REMOVED " + unicode(ne_words))

    # XXX: WordTokenize part of NLP toolkit
    words = WordTokenize(text)
    words = [w for w in words if should_stay(w)]

    LOGGER.info('TOKENS = ' + unicode(words))

    # XXX: POSTagger part of NLP toolkit
    tagger = POSTagger()
    words_posed = tagger.tag(words)

    removelist = StopWord.objects.values_list('word', flat=True)

    # XXX: Lemmatizer part of NLP toolkit
    lemmatizer = Lemmatizer()
    lemmatized_words = []
    for w, pos in words_posed:
        if pos == 'P' or pos == 'V':
            continue
        if w in removelist:
            continue
        # Add word pos here
        lem_w = lemmatizer.lemmatize(w, pos)
        LOGGER.info('1' + w + ',' + pos)
        LOGGER.info('2' + lem_w)
        lemmatized_words.append((lem_w, w))

    lemmatized_words += ne_words

    return lemmatized_words


@transaction.atomic
def write_words_to_db(words, instance):

    from models import WordCloudWord

    LOGGER.info("Un Write Words")
    LOGGER.info(len(words))
    LOGGER.info("Delete {} records", str(WordCloudWord.objects.filter(text=instance).count()))
    WordCloudWord.objects.filter(text=instance).delete()

    obj_list = []
    for w in words:
        LOGGER.info('- ' + unicode(w[0]) + ' -> ' + str(list(w[0])))
        word = WordCloudWord(
            word=w[0],
            org_word=w[1],
            text=instance,
            entity=instance.entity)
        obj_list.append(word)

    LOGGER.info(obj_list)
    WordCloudWord.objects.bulk_create(obj_list)


def process_text(instance):

    text = instance.text
    LOGGER.info('TEXT = ' + unicode(text))
    words = prepare_text(text)
    write_words_to_db(words, instance)


def wordcloudtext_saved(sender, instance, **kwargs):

    process_text(instance)


def update_all_texts():
    """
        This can be a very long process, has to be async in
        a separate thread.
    """
    from models import WordCloudText

    texts = WordCloudText.objects.all()
    for text in texts:
        process_text(text)


def run_update_all_texts():

    thread = threading.Thread(target=update_all_texts)
    thread.setDaemon(True)
    thread.start()


def stopword_deleted(sender, instance, **kwargs):

    run_update_all_texts()


def stopword_added(sender, instance, **kwargs):

    from models import WordCloudWord

    LOGGER.info("DELETE {} records".format(str(WordCloudWord.objects.filter(Q(org_word=instance.word) | Q(word=instance.word)).count())))
    WordCloudWord.objects.filter(Q(org_word=instance.word) | Q(word=instance.word)).delete()


def namedentity_changed(sender, instance, **kwargs):

    run_update_all_texts()

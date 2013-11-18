import cProfile
import simplejson as json
from collections import defaultdict
from treeherder.log_parser.artifactbuildercollection import ArtifactBuilderCollection


def parse_logs(logs, check_errors):
    for log in logs:
        artifact_builder_collection = ArtifactBuilderCollection(
            log,
            check_errors=check_errors,
        )
        artifact_builder_collection.parse()


class ParseLogProfiler(object):

    def __init__(self, configfile):
        # load the source configuration from the given file
        config = json.loads(
            configfile.read()
        )

        self.logs = defaultdict(lambda: defaultdict(dict))
        for item in config:
            self.logs[item['job_description']][item['has_failures']] = item['log_file']
        self.profile = None

    def run(self, log_type, has_failures):
        # run the profiler
        self.profile = cProfile.Profile()
        if log_type == 'all':
            log_types = self.logs.keys()
        else:
            log_types = [log_type]

        log_files = [self.logs[ltype][has_failures] for ltype in log_types]

        self.profile.runcall(parse_logs, log_files, has_failures)

    def print_stats(self):
        # this sorts the stats by internal time
        self.profile.print_stats(1)

    def dump_stats(self, filename):
        self.profile.dump_stats(filename)

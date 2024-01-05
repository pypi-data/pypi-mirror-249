import json

from protocols.protocol_8_0.cva import (
    CancerParticipantInject,
    ClinicalReportInject,
    ExitQuestionnaireInjectCancer,
    ExitQuestionnaireInjectRD,
    InterpretedGenomeInject,
    PedigreeInjectRD,
    Transaction,
)

from pyark import cva_client


class DataIntakeClient(cva_client.CvaClient):

    _INTERPRETED_GENOME_POST = "interpreted-genomes"
    _CLINICAL_REPORT_POST = "clinical-reports"
    _EXIT_QUESTIONAIRES_RD_POST = "exit-questionnaires-rd"
    _EXIT_QUESTIONAIRES_CANCER_POST = "exit-questionnaires-cancer"
    _PEDIGREE_POST = "pedigrees"
    _PARTICIPANT_POST = "participants"
    _VARIANT_INTERPRETATION_LOG = "interpretation-log"

    def __init__(self, **params):
        cva_client.CvaClient.__init__(self, **params)

    def post_pedigree(self, pedigree, params={}):
        """
        :type pedigree: PedigreeInjectRD
        :type params: dict
        :rtype: Transaction
        """
        results, _ = self._post(self._PEDIGREE_POST, pedigree.toJsonDict(), params)
        result = self._render_single_result(results, as_data_frame=False)
        return Transaction.fromJsonDict(result) if result else None

    def post_participant(self, participant, params={}):
        """
        :type participant: CancerParticipantInject
        :type params: dict
        :rtype: Transaction
        """
        results, _ = self._post(self._PARTICIPANT_POST, participant.toJsonDict(), params)
        result = self._render_single_result(results, as_data_frame=False)
        return Transaction.fromJsonDict(result) if result else None

    def post_interpreted_genome(self, tiered_variant, params={}):
        """
        :type tiered_variant: InterpretedGenomeInject
        :type params: dict
        :rtype: Transaction
        """
        results, _ = self._post(self._INTERPRETED_GENOME_POST, tiered_variant.toJsonDict(), params)
        result = self._render_single_result(results, as_data_frame=False)
        return Transaction.fromJsonDict(result) if result else None

    def post_clinical_report(self, candidate_variant, params={}):
        """
        :type candidate_variant: ClinicalReportInject
        :type params: dict
        :rtype: Transaction
        """
        candidate_variant_json = self._resolve_benign_typo(candidate_variant.toJsonDict())
        results, _ = self._post(self._CLINICAL_REPORT_POST, candidate_variant_json, params)
        result = self._render_single_result(results, as_data_frame=False)
        return Transaction.fromJsonDict(result) if result else None

    def post_exit_questionaire(self, exit_questionaire, params={}):
        """
        :type exit_questionaire: ExitQuestionnaireInjectRD
        :type params: dict
        :rtype: Transaction
        """
        results, _ = self._post(self._EXIT_QUESTIONAIRES_RD_POST, exit_questionaire.toJsonDict(), params)
        result = self._render_single_result(results, as_data_frame=False)
        return Transaction.fromJsonDict(result) if result else None

    def post_exit_questionaire_cancer(self, exit_questionaire, params={}):
        """
        :type exit_questionaire: ExitQuestionnaireInjectCancer
        :type params: dict
        :rtype: Transaction
        """
        results, _ = self._post(self._EXIT_QUESTIONAIRES_CANCER_POST, exit_questionaire.toJsonDict(), params)
        result = self._render_single_result(results, as_data_frame=False)
        return Transaction.fromJsonDict(result) if result else None

    def post_variant_interpretation_log(self, variant_interpretation_log, params={}):
        """
        :param variant_interpretation_log:
        :param params:
        :rtype: Transaction
        """
        results, _ = self._post(self._VARIANT_INTERPRETATION_LOG, variant_interpretation_log.toJsonDict(), params)
        result = self._render_single_result(results, as_data_frame=False)
        return Transaction.fromJsonDict(result) if result else None

    def _resolve_benign_typo(self, candidate_variant_json: dict) -> dict:
        """Private method which replaces all occurrences of `bening` to `benign` in
        clinical reports

        Args:
            candidate_variant_json (dict): The clinical report as a json dict

        Returns:
            dict: The json dict with all `bening` typos fixed
        """
        candidate_variant_json_string = json.dumps(candidate_variant_json)
        return json.loads(candidate_variant_json_string.replace("bening", "benign"))

from flask import request, abort

from app.api.v2 import path_2
from app.api import utils

from app.api.v2.utils import token_required, check_matching_items_in_db_table

from app.api.v2.models.offices import OfficesModel
from app.api.v2.models.users import UserModel
from app.api.v2.models.votes import VotesModel
from app.api.v2.models.candidates import CandidateModel
import psycopg2


@path_2.route("/votes", methods=["POST"])
@token_required
def create_vote(user):
    """
    a voter can vote for a particular office
    if he has hasn't voted for it yet
    """
    try:
        user_id = user[0][1]
    except:
        return utils.response_fn(401, "error", "You don't have an account")

    try:
        data = request.get_json()
        office = data["office"]
        candidate = data["candidate"]

    except KeyError:
        abort(utils.response_fn(400, "error",
                                "Should be office & candidate, enter all fields"))

    utils.check_for_ints(data, ["office", "candidate"])
    try:

        iscandidatePresent = UserModel.get_user_by_id(candidate)
        isOfficePresent = OfficesModel.get_specific_office(office)
        if iscandidatePresent and isOfficePresent:
            isCandidateRegistered = CandidateModel.check_if_candidate_is_already_registered(
                candidate, office)
            if isCandidateRegistered:
                voted = VotesModel.check_if_user_already_voted(user_id, office)
                if voted:
                    return utils.response_fn(401, "error", "You have already voted")
                newvote = VotesModel(office, candidate, user_id)
                newvote.save_vote()
                return utils.response_fn(201, "data", [{
                    "office": office,
                    "candidate": candidate,
                    "voter": user_id
                }])
            return utils.response_fn(400, "error", "This candidate is not registered for the office.")
        return utils.response_fn(404, "error", "Either Candidate or party doesn't exist")

    except psycopg2.DatabaseError as _error:
        abort(utils.response_fn(500, "error", "Server error"))


@path_2.route("/votes/activity", methods=["POST"])
@token_required
def view_activity(user):
    try:
        user_id = user[0][1]
    except:
        return utils.response_fn(401, "error", "You don't have an account")

    return utils.response_fn(200, "data", VotesModel.resolve_user_voting_activity(user_id))

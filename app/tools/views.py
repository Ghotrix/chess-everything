from flask import render_template, request, jsonify
from flask.ext.login import login_required, current_user
from . import tools
from .. import db
from ..models import User, Position, Move, UserMove, Quality
from chess import Board
from .forms import MoveForm
from random import randint as rand

@tools.route('/repertoire', methods=['GET', 'POST'])
@tools.route('/repertoire/<int:id>', methods=['GET', 'POST'])
@login_required
def repertoire(id=1):
    if request.args.get('practice'):
        print(practice(id))
    board = Board()
    form = MoveForm()
    if request.method == 'GET':
        position = Position.query.filter_by(id=id).first()
        moves = Move.query.join(User.moves).filter(User.id == current_user.id, Move.source_position_id == position.id).all()
        return render_template('tools/repertoire.html', fen=position.fen + ' 0 1', moves=moves, form=form, id=id)
    
    if request.method == 'POST':
        fen = form.append_fen.data
        san = form.append_san.data
        quality_id = form.quality.data
        board = Board(fen)
        board.push_san(san)
        source_position = Position.query.filter_by(fen=' '.join(fen.split()[:-2])).first()
        end_position_fen = ' '.join(board.fen().split()[:-2])
        end_position = Position.query.filter_by(fen=end_position_fen).first()
        if end_position is None:
            end_position = Position(fen=end_position_fen)
            db.session.add(end_position)
        move = Move.query.filter_by(source_position_id=source_position.id, destination_position_id=end_position.id).first()
        if move is None:
            move = Move(source_position_id=source_position.id, destination_position_id=end_position.id, san=san)
            um = UserMove(quality_id=quality_id)
            um.move = move
            current_user.moves.append(um)
        db.session.commit()
        moves = Move.query.join(User.moves).filter(User.id == current_user.id, Move.source_position_id == source_position.id).all()
        return render_template('tools/repertoire.html', fen=source_position.fen + ' 0 1', moves=moves, form=form, id=id)

def practice(position_id):
    t = {}
    opponents_turn = True
    last_san = 'first'
    last_pos_id = Position.query.filter_by(id=position_id).first().id
    while True:
        if opponents_turn:
            moves = Move.query.join(User.moves).filter(Move.source_position_id == last_pos_id, User.id == current_user.id).all()
            if len(moves) == 0:
                break
            rindex = rand(0, len(moves) - 1)
        else:
            moves = Move.query.join(User.moves).filter(User.id == current_user.id, Move.source_position_id == last_pos_id).filter_by(quality_id = 1).all()
            if len(moves) == 0:
                break

        if opponents_turn:
            t[last_san] = [moves[rindex].san]
        else:
            for move in moves:
                if last_san in t:
                    t[last_san] += [move.san]
                else:
                    t[last_san] = [move.san]

        opponents_turn = not opponents_turn
        last_san = moves[rindex].san
        last_pos_id = moves[rindex].destination_position_id
       
    print(t)
    return jsonify(t)

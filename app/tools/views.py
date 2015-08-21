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

@tools.route('/moves', methods = ['POST'])
@login_required
def moves():
    position_id = request.form['id']
    moves = Move.query.join(User.moves).filter(Move.source_position_id == position_id, User.id == current_user.id).all()
    #we're only need opponent's moves, that have reply (one or more)
    for move in moves:
        sub_moves = Move.query.join(User.moves).filter(Move.source_position_id == move.destination_position_id, User.id == current_user.id).filter_by(quality_id = 1).all()
        print('for src_pos {} len of submoves is {}'.format(move.destination_position_id, len(sub_moves)))
        if len(sub_moves) == 0:
            moves.remove(move)

    #in case no more replies present from opponent
    if  len(moves) == 0:
        return jsonify({'reply': 'none'})
    rindex = rand(0, len(moves) - 1)
    opponent_move = moves[rindex]
    first = opponent_move.san
    t = {}
    t['reply'] = first
    t['good_moves'] = []

    moves = Move.query.join(User.moves).filter(User.id == current_user.id, Move.source_position_id == opponent_move.destination_position_id).filter_by(quality_id = 1).all()
    
    for move in moves:
        t['good_moves'] += [[move.san, move.destination_position_id]]

    print(t)
    return jsonify(t)

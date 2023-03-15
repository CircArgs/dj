# Generated from SqlBase.g4 by ANTLR 4.9.3
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .SqlBaseParser import SqlBaseParser
else:
    from SqlBaseParser import SqlBaseParser

# This class defines a complete listener for a parse tree produced by SqlBaseParser.
class SqlBaseListener(ParseTreeListener):

    # Enter a parse tree produced by SqlBaseParser#singleStatement.
    def enterSingleStatement(self, ctx:SqlBaseParser.SingleStatementContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#singleStatement.
    def exitSingleStatement(self, ctx:SqlBaseParser.SingleStatementContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#singleExpression.
    def enterSingleExpression(self, ctx:SqlBaseParser.SingleExpressionContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#singleExpression.
    def exitSingleExpression(self, ctx:SqlBaseParser.SingleExpressionContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#singleTableIdentifier.
    def enterSingleTableIdentifier(self, ctx:SqlBaseParser.SingleTableIdentifierContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#singleTableIdentifier.
    def exitSingleTableIdentifier(self, ctx:SqlBaseParser.SingleTableIdentifierContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#singleMultipartIdentifier.
    def enterSingleMultipartIdentifier(self, ctx:SqlBaseParser.SingleMultipartIdentifierContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#singleMultipartIdentifier.
    def exitSingleMultipartIdentifier(self, ctx:SqlBaseParser.SingleMultipartIdentifierContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#singleFunctionIdentifier.
    def enterSingleFunctionIdentifier(self, ctx:SqlBaseParser.SingleFunctionIdentifierContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#singleFunctionIdentifier.
    def exitSingleFunctionIdentifier(self, ctx:SqlBaseParser.SingleFunctionIdentifierContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#singleDataType.
    def enterSingleDataType(self, ctx:SqlBaseParser.SingleDataTypeContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#singleDataType.
    def exitSingleDataType(self, ctx:SqlBaseParser.SingleDataTypeContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#statementDefault.
    def enterStatementDefault(self, ctx:SqlBaseParser.StatementDefaultContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#statementDefault.
    def exitStatementDefault(self, ctx:SqlBaseParser.StatementDefaultContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#query.
    def enterQuery(self, ctx:SqlBaseParser.QueryContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#query.
    def exitQuery(self, ctx:SqlBaseParser.QueryContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#namespace.
    def enterNamespace(self, ctx:SqlBaseParser.NamespaceContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#namespace.
    def exitNamespace(self, ctx:SqlBaseParser.NamespaceContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#ctes.
    def enterCtes(self, ctx:SqlBaseParser.CtesContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#ctes.
    def exitCtes(self, ctx:SqlBaseParser.CtesContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#namedQuery.
    def enterNamedQuery(self, ctx:SqlBaseParser.NamedQueryContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#namedQuery.
    def exitNamedQuery(self, ctx:SqlBaseParser.NamedQueryContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#queryOrganization.
    def enterQueryOrganization(self, ctx:SqlBaseParser.QueryOrganizationContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#queryOrganization.
    def exitQueryOrganization(self, ctx:SqlBaseParser.QueryOrganizationContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#queryTermDefault.
    def enterQueryTermDefault(self, ctx:SqlBaseParser.QueryTermDefaultContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#queryTermDefault.
    def exitQueryTermDefault(self, ctx:SqlBaseParser.QueryTermDefaultContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#setOperation.
    def enterSetOperation(self, ctx:SqlBaseParser.SetOperationContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#setOperation.
    def exitSetOperation(self, ctx:SqlBaseParser.SetOperationContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#queryPrimaryDefault.
    def enterQueryPrimaryDefault(self, ctx:SqlBaseParser.QueryPrimaryDefaultContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#queryPrimaryDefault.
    def exitQueryPrimaryDefault(self, ctx:SqlBaseParser.QueryPrimaryDefaultContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#fromStmt.
    def enterFromStmt(self, ctx:SqlBaseParser.FromStmtContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#fromStmt.
    def exitFromStmt(self, ctx:SqlBaseParser.FromStmtContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#subquery.
    def enterSubquery(self, ctx:SqlBaseParser.SubqueryContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#subquery.
    def exitSubquery(self, ctx:SqlBaseParser.SubqueryContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#sortItem.
    def enterSortItem(self, ctx:SqlBaseParser.SortItemContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#sortItem.
    def exitSortItem(self, ctx:SqlBaseParser.SortItemContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#fromStatement.
    def enterFromStatement(self, ctx:SqlBaseParser.FromStatementContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#fromStatement.
    def exitFromStatement(self, ctx:SqlBaseParser.FromStatementContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#fromStatementBody.
    def enterFromStatementBody(self, ctx:SqlBaseParser.FromStatementBodyContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#fromStatementBody.
    def exitFromStatementBody(self, ctx:SqlBaseParser.FromStatementBodyContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#regularQuerySpecification.
    def enterRegularQuerySpecification(self, ctx:SqlBaseParser.RegularQuerySpecificationContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#regularQuerySpecification.
    def exitRegularQuerySpecification(self, ctx:SqlBaseParser.RegularQuerySpecificationContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#selectClause.
    def enterSelectClause(self, ctx:SqlBaseParser.SelectClauseContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#selectClause.
    def exitSelectClause(self, ctx:SqlBaseParser.SelectClauseContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#assignmentList.
    def enterAssignmentList(self, ctx:SqlBaseParser.AssignmentListContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#assignmentList.
    def exitAssignmentList(self, ctx:SqlBaseParser.AssignmentListContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#assignment.
    def enterAssignment(self, ctx:SqlBaseParser.AssignmentContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#assignment.
    def exitAssignment(self, ctx:SqlBaseParser.AssignmentContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#whereClause.
    def enterWhereClause(self, ctx:SqlBaseParser.WhereClauseContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#whereClause.
    def exitWhereClause(self, ctx:SqlBaseParser.WhereClauseContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#havingClause.
    def enterHavingClause(self, ctx:SqlBaseParser.HavingClauseContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#havingClause.
    def exitHavingClause(self, ctx:SqlBaseParser.HavingClauseContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#fromClause.
    def enterFromClause(self, ctx:SqlBaseParser.FromClauseContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#fromClause.
    def exitFromClause(self, ctx:SqlBaseParser.FromClauseContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#aggregationClause.
    def enterAggregationClause(self, ctx:SqlBaseParser.AggregationClauseContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#aggregationClause.
    def exitAggregationClause(self, ctx:SqlBaseParser.AggregationClauseContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#groupingSet.
    def enterGroupingSet(self, ctx:SqlBaseParser.GroupingSetContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#groupingSet.
    def exitGroupingSet(self, ctx:SqlBaseParser.GroupingSetContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#lateralView.
    def enterLateralView(self, ctx:SqlBaseParser.LateralViewContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#lateralView.
    def exitLateralView(self, ctx:SqlBaseParser.LateralViewContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#setQuantifier.
    def enterSetQuantifier(self, ctx:SqlBaseParser.SetQuantifierContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#setQuantifier.
    def exitSetQuantifier(self, ctx:SqlBaseParser.SetQuantifierContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#relation.
    def enterRelation(self, ctx:SqlBaseParser.RelationContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#relation.
    def exitRelation(self, ctx:SqlBaseParser.RelationContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#joinRelation.
    def enterJoinRelation(self, ctx:SqlBaseParser.JoinRelationContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#joinRelation.
    def exitJoinRelation(self, ctx:SqlBaseParser.JoinRelationContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#tableName.
    def enterTableName(self, ctx:SqlBaseParser.TableNameContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#tableName.
    def exitTableName(self, ctx:SqlBaseParser.TableNameContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#aliasedQuery.
    def enterAliasedQuery(self, ctx:SqlBaseParser.AliasedQueryContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#aliasedQuery.
    def exitAliasedQuery(self, ctx:SqlBaseParser.AliasedQueryContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#aliasedRelation.
    def enterAliasedRelation(self, ctx:SqlBaseParser.AliasedRelationContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#aliasedRelation.
    def exitAliasedRelation(self, ctx:SqlBaseParser.AliasedRelationContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#tableValuedFunction.
    def enterTableValuedFunction(self, ctx:SqlBaseParser.TableValuedFunctionContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#tableValuedFunction.
    def exitTableValuedFunction(self, ctx:SqlBaseParser.TableValuedFunctionContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#joinType.
    def enterJoinType(self, ctx:SqlBaseParser.JoinTypeContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#joinType.
    def exitJoinType(self, ctx:SqlBaseParser.JoinTypeContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#joinCriteria.
    def enterJoinCriteria(self, ctx:SqlBaseParser.JoinCriteriaContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#joinCriteria.
    def exitJoinCriteria(self, ctx:SqlBaseParser.JoinCriteriaContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#identifierList.
    def enterIdentifierList(self, ctx:SqlBaseParser.IdentifierListContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#identifierList.
    def exitIdentifierList(self, ctx:SqlBaseParser.IdentifierListContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#identifierSeq.
    def enterIdentifierSeq(self, ctx:SqlBaseParser.IdentifierSeqContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#identifierSeq.
    def exitIdentifierSeq(self, ctx:SqlBaseParser.IdentifierSeqContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#orderedIdentifierList.
    def enterOrderedIdentifierList(self, ctx:SqlBaseParser.OrderedIdentifierListContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#orderedIdentifierList.
    def exitOrderedIdentifierList(self, ctx:SqlBaseParser.OrderedIdentifierListContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#orderedIdentifier.
    def enterOrderedIdentifier(self, ctx:SqlBaseParser.OrderedIdentifierContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#orderedIdentifier.
    def exitOrderedIdentifier(self, ctx:SqlBaseParser.OrderedIdentifierContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#functionTable.
    def enterFunctionTable(self, ctx:SqlBaseParser.FunctionTableContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#functionTable.
    def exitFunctionTable(self, ctx:SqlBaseParser.FunctionTableContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#tableAlias.
    def enterTableAlias(self, ctx:SqlBaseParser.TableAliasContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#tableAlias.
    def exitTableAlias(self, ctx:SqlBaseParser.TableAliasContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#multipartIdentifierList.
    def enterMultipartIdentifierList(self, ctx:SqlBaseParser.MultipartIdentifierListContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#multipartIdentifierList.
    def exitMultipartIdentifierList(self, ctx:SqlBaseParser.MultipartIdentifierListContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#multipartIdentifier.
    def enterMultipartIdentifier(self, ctx:SqlBaseParser.MultipartIdentifierContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#multipartIdentifier.
    def exitMultipartIdentifier(self, ctx:SqlBaseParser.MultipartIdentifierContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#tableIdentifier.
    def enterTableIdentifier(self, ctx:SqlBaseParser.TableIdentifierContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#tableIdentifier.
    def exitTableIdentifier(self, ctx:SqlBaseParser.TableIdentifierContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#functionIdentifier.
    def enterFunctionIdentifier(self, ctx:SqlBaseParser.FunctionIdentifierContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#functionIdentifier.
    def exitFunctionIdentifier(self, ctx:SqlBaseParser.FunctionIdentifierContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#namedExpression.
    def enterNamedExpression(self, ctx:SqlBaseParser.NamedExpressionContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#namedExpression.
    def exitNamedExpression(self, ctx:SqlBaseParser.NamedExpressionContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#namedExpressionSeq.
    def enterNamedExpressionSeq(self, ctx:SqlBaseParser.NamedExpressionSeqContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#namedExpressionSeq.
    def exitNamedExpressionSeq(self, ctx:SqlBaseParser.NamedExpressionSeqContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#expression.
    def enterExpression(self, ctx:SqlBaseParser.ExpressionContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#expression.
    def exitExpression(self, ctx:SqlBaseParser.ExpressionContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#logicalNot.
    def enterLogicalNot(self, ctx:SqlBaseParser.LogicalNotContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#logicalNot.
    def exitLogicalNot(self, ctx:SqlBaseParser.LogicalNotContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#predicated.
    def enterPredicated(self, ctx:SqlBaseParser.PredicatedContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#predicated.
    def exitPredicated(self, ctx:SqlBaseParser.PredicatedContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#exists.
    def enterExists(self, ctx:SqlBaseParser.ExistsContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#exists.
    def exitExists(self, ctx:SqlBaseParser.ExistsContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#logicalBinary.
    def enterLogicalBinary(self, ctx:SqlBaseParser.LogicalBinaryContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#logicalBinary.
    def exitLogicalBinary(self, ctx:SqlBaseParser.LogicalBinaryContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#predicate.
    def enterPredicate(self, ctx:SqlBaseParser.PredicateContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#predicate.
    def exitPredicate(self, ctx:SqlBaseParser.PredicateContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#valueExpressionDefault.
    def enterValueExpressionDefault(self, ctx:SqlBaseParser.ValueExpressionDefaultContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#valueExpressionDefault.
    def exitValueExpressionDefault(self, ctx:SqlBaseParser.ValueExpressionDefaultContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#comparison.
    def enterComparison(self, ctx:SqlBaseParser.ComparisonContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#comparison.
    def exitComparison(self, ctx:SqlBaseParser.ComparisonContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#arithmeticBinary.
    def enterArithmeticBinary(self, ctx:SqlBaseParser.ArithmeticBinaryContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#arithmeticBinary.
    def exitArithmeticBinary(self, ctx:SqlBaseParser.ArithmeticBinaryContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#arithmeticUnary.
    def enterArithmeticUnary(self, ctx:SqlBaseParser.ArithmeticUnaryContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#arithmeticUnary.
    def exitArithmeticUnary(self, ctx:SqlBaseParser.ArithmeticUnaryContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#struct.
    def enterStruct(self, ctx:SqlBaseParser.StructContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#struct.
    def exitStruct(self, ctx:SqlBaseParser.StructContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#dereference.
    def enterDereference(self, ctx:SqlBaseParser.DereferenceContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#dereference.
    def exitDereference(self, ctx:SqlBaseParser.DereferenceContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#simpleCase.
    def enterSimpleCase(self, ctx:SqlBaseParser.SimpleCaseContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#simpleCase.
    def exitSimpleCase(self, ctx:SqlBaseParser.SimpleCaseContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#columnReference.
    def enterColumnReference(self, ctx:SqlBaseParser.ColumnReferenceContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#columnReference.
    def exitColumnReference(self, ctx:SqlBaseParser.ColumnReferenceContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#rowConstructor.
    def enterRowConstructor(self, ctx:SqlBaseParser.RowConstructorContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#rowConstructor.
    def exitRowConstructor(self, ctx:SqlBaseParser.RowConstructorContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#last.
    def enterLast(self, ctx:SqlBaseParser.LastContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#last.
    def exitLast(self, ctx:SqlBaseParser.LastContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#star.
    def enterStar(self, ctx:SqlBaseParser.StarContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#star.
    def exitStar(self, ctx:SqlBaseParser.StarContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#overlay.
    def enterOverlay(self, ctx:SqlBaseParser.OverlayContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#overlay.
    def exitOverlay(self, ctx:SqlBaseParser.OverlayContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#subscript.
    def enterSubscript(self, ctx:SqlBaseParser.SubscriptContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#subscript.
    def exitSubscript(self, ctx:SqlBaseParser.SubscriptContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#subqueryExpression.
    def enterSubqueryExpression(self, ctx:SqlBaseParser.SubqueryExpressionContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#subqueryExpression.
    def exitSubqueryExpression(self, ctx:SqlBaseParser.SubqueryExpressionContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#substring.
    def enterSubstring(self, ctx:SqlBaseParser.SubstringContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#substring.
    def exitSubstring(self, ctx:SqlBaseParser.SubstringContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#currentDatetime.
    def enterCurrentDatetime(self, ctx:SqlBaseParser.CurrentDatetimeContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#currentDatetime.
    def exitCurrentDatetime(self, ctx:SqlBaseParser.CurrentDatetimeContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#cast.
    def enterCast(self, ctx:SqlBaseParser.CastContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#cast.
    def exitCast(self, ctx:SqlBaseParser.CastContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#constantDefault.
    def enterConstantDefault(self, ctx:SqlBaseParser.ConstantDefaultContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#constantDefault.
    def exitConstantDefault(self, ctx:SqlBaseParser.ConstantDefaultContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#lambda.
    def enterLambda(self, ctx:SqlBaseParser.LambdaContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#lambda.
    def exitLambda(self, ctx:SqlBaseParser.LambdaContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#parenthesizedExpression.
    def enterParenthesizedExpression(self, ctx:SqlBaseParser.ParenthesizedExpressionContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#parenthesizedExpression.
    def exitParenthesizedExpression(self, ctx:SqlBaseParser.ParenthesizedExpressionContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#extract.
    def enterExtract(self, ctx:SqlBaseParser.ExtractContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#extract.
    def exitExtract(self, ctx:SqlBaseParser.ExtractContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#trim.
    def enterTrim(self, ctx:SqlBaseParser.TrimContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#trim.
    def exitTrim(self, ctx:SqlBaseParser.TrimContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#functionCall.
    def enterFunctionCall(self, ctx:SqlBaseParser.FunctionCallContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#functionCall.
    def exitFunctionCall(self, ctx:SqlBaseParser.FunctionCallContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#searchedCase.
    def enterSearchedCase(self, ctx:SqlBaseParser.SearchedCaseContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#searchedCase.
    def exitSearchedCase(self, ctx:SqlBaseParser.SearchedCaseContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#position.
    def enterPosition(self, ctx:SqlBaseParser.PositionContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#position.
    def exitPosition(self, ctx:SqlBaseParser.PositionContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#first.
    def enterFirst(self, ctx:SqlBaseParser.FirstContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#first.
    def exitFirst(self, ctx:SqlBaseParser.FirstContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#nullLiteral.
    def enterNullLiteral(self, ctx:SqlBaseParser.NullLiteralContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#nullLiteral.
    def exitNullLiteral(self, ctx:SqlBaseParser.NullLiteralContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#intervalLiteral.
    def enterIntervalLiteral(self, ctx:SqlBaseParser.IntervalLiteralContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#intervalLiteral.
    def exitIntervalLiteral(self, ctx:SqlBaseParser.IntervalLiteralContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#numericLiteral.
    def enterNumericLiteral(self, ctx:SqlBaseParser.NumericLiteralContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#numericLiteral.
    def exitNumericLiteral(self, ctx:SqlBaseParser.NumericLiteralContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#booleanLiteral.
    def enterBooleanLiteral(self, ctx:SqlBaseParser.BooleanLiteralContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#booleanLiteral.
    def exitBooleanLiteral(self, ctx:SqlBaseParser.BooleanLiteralContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#stringLiteral.
    def enterStringLiteral(self, ctx:SqlBaseParser.StringLiteralContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#stringLiteral.
    def exitStringLiteral(self, ctx:SqlBaseParser.StringLiteralContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#comparisonOperator.
    def enterComparisonOperator(self, ctx:SqlBaseParser.ComparisonOperatorContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#comparisonOperator.
    def exitComparisonOperator(self, ctx:SqlBaseParser.ComparisonOperatorContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#arithmeticOperator.
    def enterArithmeticOperator(self, ctx:SqlBaseParser.ArithmeticOperatorContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#arithmeticOperator.
    def exitArithmeticOperator(self, ctx:SqlBaseParser.ArithmeticOperatorContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#predicateOperator.
    def enterPredicateOperator(self, ctx:SqlBaseParser.PredicateOperatorContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#predicateOperator.
    def exitPredicateOperator(self, ctx:SqlBaseParser.PredicateOperatorContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#booleanValue.
    def enterBooleanValue(self, ctx:SqlBaseParser.BooleanValueContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#booleanValue.
    def exitBooleanValue(self, ctx:SqlBaseParser.BooleanValueContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#interval.
    def enterInterval(self, ctx:SqlBaseParser.IntervalContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#interval.
    def exitInterval(self, ctx:SqlBaseParser.IntervalContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#errorCapturingMultiUnitsInterval.
    def enterErrorCapturingMultiUnitsInterval(self, ctx:SqlBaseParser.ErrorCapturingMultiUnitsIntervalContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#errorCapturingMultiUnitsInterval.
    def exitErrorCapturingMultiUnitsInterval(self, ctx:SqlBaseParser.ErrorCapturingMultiUnitsIntervalContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#multiUnitsInterval.
    def enterMultiUnitsInterval(self, ctx:SqlBaseParser.MultiUnitsIntervalContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#multiUnitsInterval.
    def exitMultiUnitsInterval(self, ctx:SqlBaseParser.MultiUnitsIntervalContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#errorCapturingUnitToUnitInterval.
    def enterErrorCapturingUnitToUnitInterval(self, ctx:SqlBaseParser.ErrorCapturingUnitToUnitIntervalContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#errorCapturingUnitToUnitInterval.
    def exitErrorCapturingUnitToUnitInterval(self, ctx:SqlBaseParser.ErrorCapturingUnitToUnitIntervalContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#unitToUnitInterval.
    def enterUnitToUnitInterval(self, ctx:SqlBaseParser.UnitToUnitIntervalContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#unitToUnitInterval.
    def exitUnitToUnitInterval(self, ctx:SqlBaseParser.UnitToUnitIntervalContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#intervalValue.
    def enterIntervalValue(self, ctx:SqlBaseParser.IntervalValueContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#intervalValue.
    def exitIntervalValue(self, ctx:SqlBaseParser.IntervalValueContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#intervalUnit.
    def enterIntervalUnit(self, ctx:SqlBaseParser.IntervalUnitContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#intervalUnit.
    def exitIntervalUnit(self, ctx:SqlBaseParser.IntervalUnitContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#complexDataType.
    def enterComplexDataType(self, ctx:SqlBaseParser.ComplexDataTypeContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#complexDataType.
    def exitComplexDataType(self, ctx:SqlBaseParser.ComplexDataTypeContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#primitiveDataType.
    def enterPrimitiveDataType(self, ctx:SqlBaseParser.PrimitiveDataTypeContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#primitiveDataType.
    def exitPrimitiveDataType(self, ctx:SqlBaseParser.PrimitiveDataTypeContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#complexColTypeList.
    def enterComplexColTypeList(self, ctx:SqlBaseParser.ComplexColTypeListContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#complexColTypeList.
    def exitComplexColTypeList(self, ctx:SqlBaseParser.ComplexColTypeListContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#complexColType.
    def enterComplexColType(self, ctx:SqlBaseParser.ComplexColTypeContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#complexColType.
    def exitComplexColType(self, ctx:SqlBaseParser.ComplexColTypeContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#whenClause.
    def enterWhenClause(self, ctx:SqlBaseParser.WhenClauseContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#whenClause.
    def exitWhenClause(self, ctx:SqlBaseParser.WhenClauseContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#windowClause.
    def enterWindowClause(self, ctx:SqlBaseParser.WindowClauseContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#windowClause.
    def exitWindowClause(self, ctx:SqlBaseParser.WindowClauseContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#namedWindow.
    def enterNamedWindow(self, ctx:SqlBaseParser.NamedWindowContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#namedWindow.
    def exitNamedWindow(self, ctx:SqlBaseParser.NamedWindowContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#windowRef.
    def enterWindowRef(self, ctx:SqlBaseParser.WindowRefContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#windowRef.
    def exitWindowRef(self, ctx:SqlBaseParser.WindowRefContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#windowDef.
    def enterWindowDef(self, ctx:SqlBaseParser.WindowDefContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#windowDef.
    def exitWindowDef(self, ctx:SqlBaseParser.WindowDefContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#windowFrame.
    def enterWindowFrame(self, ctx:SqlBaseParser.WindowFrameContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#windowFrame.
    def exitWindowFrame(self, ctx:SqlBaseParser.WindowFrameContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#frameBound.
    def enterFrameBound(self, ctx:SqlBaseParser.FrameBoundContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#frameBound.
    def exitFrameBound(self, ctx:SqlBaseParser.FrameBoundContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#qualifiedNameList.
    def enterQualifiedNameList(self, ctx:SqlBaseParser.QualifiedNameListContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#qualifiedNameList.
    def exitQualifiedNameList(self, ctx:SqlBaseParser.QualifiedNameListContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#functionName.
    def enterFunctionName(self, ctx:SqlBaseParser.FunctionNameContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#functionName.
    def exitFunctionName(self, ctx:SqlBaseParser.FunctionNameContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#qualifiedName.
    def enterQualifiedName(self, ctx:SqlBaseParser.QualifiedNameContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#qualifiedName.
    def exitQualifiedName(self, ctx:SqlBaseParser.QualifiedNameContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#errorCapturingIdentifier.
    def enterErrorCapturingIdentifier(self, ctx:SqlBaseParser.ErrorCapturingIdentifierContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#errorCapturingIdentifier.
    def exitErrorCapturingIdentifier(self, ctx:SqlBaseParser.ErrorCapturingIdentifierContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#errorIdent.
    def enterErrorIdent(self, ctx:SqlBaseParser.ErrorIdentContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#errorIdent.
    def exitErrorIdent(self, ctx:SqlBaseParser.ErrorIdentContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#realIdent.
    def enterRealIdent(self, ctx:SqlBaseParser.RealIdentContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#realIdent.
    def exitRealIdent(self, ctx:SqlBaseParser.RealIdentContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#identifier.
    def enterIdentifier(self, ctx:SqlBaseParser.IdentifierContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#identifier.
    def exitIdentifier(self, ctx:SqlBaseParser.IdentifierContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#unquotedIdentifier.
    def enterUnquotedIdentifier(self, ctx:SqlBaseParser.UnquotedIdentifierContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#unquotedIdentifier.
    def exitUnquotedIdentifier(self, ctx:SqlBaseParser.UnquotedIdentifierContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#quotedIdentifierAlternative.
    def enterQuotedIdentifierAlternative(self, ctx:SqlBaseParser.QuotedIdentifierAlternativeContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#quotedIdentifierAlternative.
    def exitQuotedIdentifierAlternative(self, ctx:SqlBaseParser.QuotedIdentifierAlternativeContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#quotedIdentifier.
    def enterQuotedIdentifier(self, ctx:SqlBaseParser.QuotedIdentifierContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#quotedIdentifier.
    def exitQuotedIdentifier(self, ctx:SqlBaseParser.QuotedIdentifierContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#exponentLiteral.
    def enterExponentLiteral(self, ctx:SqlBaseParser.ExponentLiteralContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#exponentLiteral.
    def exitExponentLiteral(self, ctx:SqlBaseParser.ExponentLiteralContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#decimalLiteral.
    def enterDecimalLiteral(self, ctx:SqlBaseParser.DecimalLiteralContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#decimalLiteral.
    def exitDecimalLiteral(self, ctx:SqlBaseParser.DecimalLiteralContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#legacyDecimalLiteral.
    def enterLegacyDecimalLiteral(self, ctx:SqlBaseParser.LegacyDecimalLiteralContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#legacyDecimalLiteral.
    def exitLegacyDecimalLiteral(self, ctx:SqlBaseParser.LegacyDecimalLiteralContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#integerLiteral.
    def enterIntegerLiteral(self, ctx:SqlBaseParser.IntegerLiteralContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#integerLiteral.
    def exitIntegerLiteral(self, ctx:SqlBaseParser.IntegerLiteralContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#bigIntLiteral.
    def enterBigIntLiteral(self, ctx:SqlBaseParser.BigIntLiteralContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#bigIntLiteral.
    def exitBigIntLiteral(self, ctx:SqlBaseParser.BigIntLiteralContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#smallIntLiteral.
    def enterSmallIntLiteral(self, ctx:SqlBaseParser.SmallIntLiteralContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#smallIntLiteral.
    def exitSmallIntLiteral(self, ctx:SqlBaseParser.SmallIntLiteralContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#tinyIntLiteral.
    def enterTinyIntLiteral(self, ctx:SqlBaseParser.TinyIntLiteralContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#tinyIntLiteral.
    def exitTinyIntLiteral(self, ctx:SqlBaseParser.TinyIntLiteralContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#doubleLiteral.
    def enterDoubleLiteral(self, ctx:SqlBaseParser.DoubleLiteralContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#doubleLiteral.
    def exitDoubleLiteral(self, ctx:SqlBaseParser.DoubleLiteralContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#bigDecimalLiteral.
    def enterBigDecimalLiteral(self, ctx:SqlBaseParser.BigDecimalLiteralContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#bigDecimalLiteral.
    def exitBigDecimalLiteral(self, ctx:SqlBaseParser.BigDecimalLiteralContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#ansiNonReserved.
    def enterAnsiNonReserved(self, ctx:SqlBaseParser.AnsiNonReservedContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#ansiNonReserved.
    def exitAnsiNonReserved(self, ctx:SqlBaseParser.AnsiNonReservedContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#strictNonReserved.
    def enterStrictNonReserved(self, ctx:SqlBaseParser.StrictNonReservedContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#strictNonReserved.
    def exitStrictNonReserved(self, ctx:SqlBaseParser.StrictNonReservedContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#nonReserved.
    def enterNonReserved(self, ctx:SqlBaseParser.NonReservedContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#nonReserved.
    def exitNonReserved(self, ctx:SqlBaseParser.NonReservedContext):
        pass



del SqlBaseParser
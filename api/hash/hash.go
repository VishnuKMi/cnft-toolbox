package hash

import (
	"github.com/ton-community/compressed-nft-api/types"
	"github.com/xssnick/tonutils-go/tvm/cell"
)

var ZeroNodes []types.Node

func init() {
	ZeroNodes = append(ZeroNodes, types.NewNode(make([]byte, 32)))
	for i := 1; i < types.MAX_LEVELS; i++ {
		ZeroNodes = append(ZeroNodes, Nodes(ZeroNodes[i-1], ZeroNodes[i-1]))
	}
}

func Nodes(a, b types.Node) types.Node {
	return types.NewNode(cell.BeginCell().MustStoreSlice(a.Hash[:], uint(len(a.Hash))*8).MustStoreSlice(b.Hash[:], uint(len(b.Hash))*8).EndCell().Hash())
}
